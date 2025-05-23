import os
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey

# Настройки
TOKEN_MINT = os.getenv("TOKEN_MINT")
MAIN_WALLET = os.getenv("MAIN_WALLET")
PRIVATE_KEYS = [
    os.getenv("PRIVATE_KEY_1"),
    os.getenv("PRIVATE_KEY_2"),
    os.getenv("PRIVATE_KEY_3"),
]

client = Client("https://api.mainnet-beta.solana.com")

def pump_logic():
    print(f"Starting pump on token: {TOKEN_MINT}")
    print(f"Main wallet: {MAIN_WALLET}")
    for i, pk in enumerate(PRIVATE_KEYS, 1):
        if pk:
            print(f"Using wallet {i} to trade...")

if __name__ == "__main__":
    pump_logic()
