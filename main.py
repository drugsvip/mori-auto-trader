import os
import time
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey

# Settings
TOKEN_MINT = os.getenv("TOKEN_MINT")
MAIN_WALLET = os.getenv("MAIN_WALLET")
PRIVATE_KEYS = [
    os.getenv("PRIVATE_KEY_1"),
    os.getenv("PRIVATE_KEY_2"),
    os.getenv("PRIVATE_KEY_3")
]

# Pump Logic with dynamic delays and spends
TIMEFRAMES = [60, 180, 180, 420, 180, 120]  # in seconds
SPENDS = [0.004, 0.003, 0.001, 0.002, 0.004, 0.003]

def pump_logic():
    print(f"Starting pump on token: {TOKEN_MINT}")
    print(f"Main wallet: {MAIN_WALLET}")
    client = Client("https://api.mainnet-beta.solana.com")

    i = 0
    while True:
        try:
            for idx, pk in enumerate(PRIVATE_KEYS):
                if not pk:
                    continue
                wallet = Keypair.from_base58_string(pk)
                pubkey = wallet.pubkey()
                amount = SPENDS[i % len(SPENDS)]
                timeframe = TIMEFRAMES[i % len(TIMEFRAMES)]

                print(f"[{idx}] Buying {amount} SOL worth of {TOKEN_MINT} from wallet {pubkey}...")

                # Placeholder for trade logic
                # response = client.send_transaction(...)

                i += 1
                time.sleep(timeframe)
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(60)

if __name__ == "__main__":
    pump_logic()
