import os
import time
import logging
import requests
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solders.rpc.config import RpcSendTransactionConfig
from solana.rpc.async_api import AsyncClient

# Настройка логирования с текущей датой
current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
log_file = f"bot_{current_time}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_file)
    ]
)
logger = logging.getLogger(__name__)

# Загрузка переменных
load_dotenv()
TOKEN_MINT = os.getenv("TOKEN_MINT", "CrTNwtygzRQkpHAQbEsNAyNdiMUAsSWRcMakP81jpump")
MAIN_WALLET = os.getenv("MAIN_WALLET", "4Qvt9SabWos2JDx9PvjUywoyy9vXvSgBJ4KcRMcqzvm9")
PRIVATE_KEYS = [pk for pk in [os.getenv(f"PRIVATE_KEY_{i}") for i in range(1, 4)] if pk]
RPC_ENDPOINT = os.getenv("RPC_ENDPOINT", "https://pit36.nodes.rpcpool.com")
MIN_BALANCE_FOR_TX = int(0.00015 * 1_000_000_000)  # Минимальный баланс в lamports (int)

if not PRIVATE_KEYS:
    logger.error("No private keys found. Exiting.")
    exit(1)

main_wallet = Pubkey.from_string(MAIN_WALLET)
keypairs = [Keypair.from_base58_string(pk) for pk in PRIVATE_KEYS]
client = AsyncClient(RPC_ENDPOINT)

DELAYS = [60, 180, 180, 420, 180, 120]
AMOUNTS = [0.004, 0.003, 0.001, 0.002, 0.004, 0.003]
SLIPPAGE_BPS = 100
TIMEOUT = 15

async def get_balance(pubkey: Pubkey) -> int:  # Возвращаем int вместо Lamports
    try:
        balance = await client.get_balance(pubkey)
        return balance.value  # Возвращает int (lamports)
    except Exception as e:
        logger.error(f"Balance error: {e}")
        return 0

async def send_transaction(from_keypair: Keypair, to_pubkey: Pubkey, amount_sol: float) -> str | None:
    try:
        balance = await get_balance(from_keypair.pubkey())
        amount_lamports = int(amount_sol * 1_000_000_000)
        required_balance = amount_lamports + MIN_BALANCE_FOR_TX
        if balance < required_balance:
            logger.error(f"Not enough balance: {balance / 1_000_000_000:.6f} < {amount_sol + 0.00015:.6f} SOL")
            return None

        txn = Transaction().add(
            transfer(
                TransferParams(
                    from_pubkey=from_keypair.pubkey(),
                    to_pubkey=to_pubkey,
                    lamports=amount_lamports
                )
            )
        )
        response = await client.send_transaction(
            txn, from_keypair, config=RpcSendTransactionConfig(skip_preflight=False)
        )
        await client.confirm_transaction(response.value)  # Ожидание подтверждения
        logger.info(f"Transaction sent: {response.value} | {from_keypair.pubkey()} → {to_pubkey} ({amount_sol} SOL)")
        return str(response.value)
    except Exception as e:
        logger.error(f"TX error: {e}")
        return None

async def swap_on_jupiter(from_keypair: Keypair, amount_sol: float, token_mint: str) -> str | None:
    try:
        quote = requests.get(
            "https://quote-api.jup.ag/v6/quote",
            params={
                "inputMint": "So11111111111111111111111111111111111111112",
                "outputMint": token_mint,
                "amount": int(amount_sol * 1_000_000_000),
                "slippageBps": SLIPPAGE_BPS
            },
            timeout=TIMEOUT
        ).json()

        if "error" in quote:
            logger.error(f"Quote error: {quote['error']}")
            return None

        response = requests.post(
            "https://quote-api.jup.ag/v6/swap",
            json={
                "quoteResponse": quote,
                "userPublicKey": str(from_keypair.pubkey()),
                "wrapAndUnwrapSol": True
            },
            timeout=TIMEOUT
        ).json()

        if "error" in response:
            logger.error(f"Swap error: {response['error']}")
            return None

        swap_tx = response["swapTransaction"]
        if not swap_tx or len(swap_tx) < 100:  # Проверка на валидность
            logger.error("Invalid swap transaction received")
            return None

        txn = Transaction.deserialize(bytes.fromhex(swap_tx))
        txid = await client.send_transaction(txn, from_keypair)
        await client.confirm_transaction(txid.value)  # Ожидание подтверждения
        logger.info(f"Swap executed: {txid.value}")
        return str(txid.value)
    except Exception as e:
        logger.error(f"Swap exception: {e}")
        return None

async def main():
    import asyncio
    cycle = 0
    successful = 0
    while True:
        try:
            cycle += 1
            logger.info(f"Cycle {cycle} started at {time.strftime('%H:%M:%S', time.gmtime())} UTC")
            for i, (delay, amount) in enumerate(zip(DELAYS, AMOUNTS)):
                for kp in keypairs:
                    logger.info(f"[Cycle {cycle} / Step {i+1}] {kp.pubkey()} → {main_wallet} | {amount} SOL")
                    txid = await send_transaction(kp, main_wallet, amount)
                    if txid:
                        swap_tx = await swap_on_jupiter(kp, amount, TOKEN_MINT)
                        if swap_tx:
                            successful += 1
                    await asyncio.sleep(delay)
            logger.info(f"Cycle {cycle} complete at {time.strftime('%H:%M:%S', time.gmtime())} UTC. Successful TXs: {successful}")
        except Exception as e:
            logger.error(f"Main loop error: {e}. Restarting in 60 seconds...")
            await asyncio.sleep(60)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
