import os
import time
import requests
from solders.keypair import Keypair
from base64 import b64decode

RPC = "https://api.mainnet-beta.solana.com"
TOKEN_MINT = os.getenv("TOKEN_MINT")
MAIN_WALLET = os.getenv("MAIN_WALLET")
PRIVATE_KEYS = [
    os.getenv("PRIVATE_KEY_1"),
    os.getenv("PRIVATE_KEY_2"),
    os.getenv("PRIVATE_KEY_3")
]

SOL_MINT = "So11111111111111111111111111111111111111112"
INTERVALS = [60, 180, 180, 420, 180, 120]
AMOUNTS = [0.004, 0.003, 0.001, 0.002, 0.004, 0.003]

def jupiter_swap(pubkey, amount_lamports):
    try:
        url = "https://quote-api.jup.ag/v6/swap"
        params = {
            "inputMint": SOL_MINT,
            "outputMint": TOKEN_MINT,
            "amount": int(amount_lamports),
            "slippage": 1,
            "userPublicKey": str(pubkey),
            "onlyDirectRoutes": True
        }
        r = requests.get(url, params=params)
        quote = r.json()
        print(f"Quote received for {amount_lamports / 1e9} SOL swap: {quote.get('outAmount')} units of MORI")
    except Exception as e:
        print(f"Swap error: {e}")

def run():
    print("=== MORI PUMP BOT STARTED ===")
    wallets = [Keypair.from_bytes(b64decode(k)) for k in PRIVATE_KEYS if k]
    i = 0
    while True:
        for wallet in wallets:
            amt = int(AMOUNTS[i % len(AMOUNTS)] * 1e9)
            interval = INTERVALS[i % len(INTERVALS)]
            pub = wallet.pubkey()
            print(f"Swapping {amt / 1e9} SOL from wallet {pub}...")
            jupiter_swap(pub, amt)
            print(f"Sleeping {interval} sec")
            time.sleep(interval)
            i += 1

if __name__ == "__main__":
    run()