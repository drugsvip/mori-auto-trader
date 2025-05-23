# mori-auto-trader

Pump bot for MORI token on Solana (Render background worker).

## Setup

Set these environment variables on Render:

- PRIVATE_KEY_1
- PRIVATE_KEY_2
- PRIVATE_KEY_3
- MAIN_WALLET
- TOKEN_MINT

Deploy as a background worker with:

```
pip install -r requirements.txt
python main.py
```