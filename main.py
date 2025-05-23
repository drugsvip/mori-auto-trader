import time
import requests

TOKEN = "CrTNwtygzRQkpHAQbEsNAyNdiMUAsSWRcMakP81jpump"
WALLET = "4Qvt9SabWos2JDx9PvjUywoyy9vXvSgBJ4KcRMcqzvm9"
RPC = "https://api.mainnet-beta.solana.com"

def buy_mori():
    print("Buying MORI... (фейк-логика)")
    # Тут вставляется реальный вызов торгового API, если будет

def sell_mori():
    print("Selling MORI... (фейк-логика)")
    # Здесь реализация для продажи MORI

def trade_loop():
    print("Запуск MORI трейдера...")
    while True:
        try:
            buy_mori()
            time.sleep(10)  # Ждём
            sell_mori()
            time.sleep(20)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(30)

if __name__ == "__main__":
    trade_loop()
