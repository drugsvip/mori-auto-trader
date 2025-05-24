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
  pip install --upgrade pip && pip install -r requirements.txt
