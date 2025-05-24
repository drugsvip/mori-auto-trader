# MORI Pump Bot (Full GitHub + Render Ready)

## Описание
Этот бот генерирует активность в сети Solana для токена MORI:
- переводит SOL от рабочих кошельков,
- выполняет свапы через Jupiter API (SOL -> MORI),
- логирует в консоль и файл,
- полностью готов к загрузке на GitHub и запуску на Render.com.

## Установка

### Render.com (Background Worker)
1. Создайте репозиторий на GitHub и загрузите эти файлы.
2. Зайдите на [https://render.com](https://render.com) и создайте новый **Background Worker**.
3. Подключите ваш репозиторий.
4. Укажите:
- Build Command:
  ```bash
  pip install -r requirements.txt
  ```
- Start Command:
  ```bash
  python main.py
  ```
5. Добавьте переменные окружения из `.env` (или подключите сам `.env` если используете Docker).

## Переменные окружения
```
TOKEN_MINT=<токен MORI>
MAIN_WALLET=<основной кошелек>
PRIVATE_KEY_1=<рабочий ключ 1>
PRIVATE_KEY_2=<рабочий ключ 2>
PRIVATE_KEY_3=<рабочий ключ 3>
RPC_ENDPOINT=https://pit36.nodes.rpcpool.com
```

## Логи
- Все действия логируются в файл с меткой времени: `bot_YYYY-MM-DD_HH-MM-SS.log`
- Также видно в логе Render

## Лицензия
MIT или любая на ваш выбор
