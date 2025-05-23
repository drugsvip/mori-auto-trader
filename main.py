import os
import time
import logging
import requests
import base64
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from dotenv import load_dotenv
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction as SolanaTransaction
from solana.system_program import TransferParams, transfer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

TOKEN_MINT = os.getenv("TOKEN_MINT")
MAIN_WALLET = os.getenv("MAIN_WALLET")
PRIVATE_KEYS = [
    os.getenv("PRIVATE_KEY_1"),
    os.getenv("PRIVATE_KEY_2"),
    os.getenv("PRIVATE_KEY_3")
]

if not all([TOKEN_MINT, MAIN_WALLET] + PRIVATE_KEYS):
    logger.error("Одна или несколько переменных окружения не заданы")
    exit(1)

main_wallet = Pubkey.from_string(MAIN_WALLET)
keypairs = [Keypair.from_base58_string(pk) for pk in PRIVATE_KEYS if pk]

DELAYS = [1, 3, 3, 7, 3, 2]
AMOUNTS = [0.004, 0.003, 0.001, 0.002, 0.003, 0.002]
LAMPORTS_PER_SOL = 1_000_000_000
RPC_URL = "https://api.mainnet-beta.solana.com"

async def send_transaction(from_keypair: Keypair, to_pubkey: Pubkey, amount_sol: float, client):
    try:
        amount_lamports = int(amount_sol * LAMPORTS_PER_SOL)
        txn = SolanaTransaction().add(
            transfer(
                TransferParams(
                    from_pubkey=from_keypair.pubkey(),
                    to_pubkey=to_pubkey,
                    lamports=amount_lamports
                )
            )
        )
        response = await client.send_transaction(txn, from_keypair)
        logger.info(f"TX отправлен: {response.value} | {from_keypair.pubkey()} → {to_pubkey} | {amount_sol} SOL")
        return response.value
    except Exception as e:
        logger.error(f"TX ошибка: {e}")
        return None

async def swap_on_dex(from_keypair: Keypair, amount_sol: float, token_mint: str, client):
    try:
        pubkey_str = str(from_keypair.pubkey())
        quote_url = "https://quote-api.jup.ag/v6/quote"
        params = {
            "inputMint": "So11111111111111111111111111111111111111112",
            "outputMint": token_mint,
            "amount": int(amount_sol * LAMPORTS_PER_SOL),
            "slippageBps": 50
        }
        quote = requests.get(quote_url, params=params).json()

        swap_url = "https://quote-api.jup.ag/v6/swap"
        swap_data = {
            "quoteResponse": quote,
            "userPublicKey": pubkey_str,
            "wrapAndUnwrapSol": True,
            "swapMode": "ExactIn"
        }
        swap_response = requests.post(swap_url, json=swap_data).json()
        swap_tx = swap_response["swapTransaction"]

        txn = Transaction.deserialize(base64.b64decode(swap_tx))
        tx_result = await client.send_transaction(txn, from_keypair)
        logger.info(f"Свап выполнен: {tx_result.value}")
        return tx_result.value
    except Exception as e:
        logger.error(f"Ошибка свапа: {e}")
        return None

async def main():
    import asyncio
    cycle = 0
    client = AsyncClient(RPC_URL)
    while True:
        for i, (delay, amount) in enumerate(zip(DELAYS, AMOUNTS)):
            for keypair in keypairs:
                logger.info(f"[Цикл {cycle+1}] Кошелёк: {keypair.pubkey()} | {amount} SOL")
                await send_transaction(keypair, main_wallet, amount, client)
                await swap_on_dex(keypair, amount, TOKEN_MINT, client)
                logger.info(f"Ожидание {delay} минут")
                await asyncio.sleep(delay * 60)
        cycle += 1

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())