import os
import asyncio
import logging
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Flask-приложение
app = Flask(__name__)

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в переменных окружения!")

# Инициализируем Telegram Application
application = ApplicationBuilder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я успешно запущен через Webhook на Render 🎉")

# Обработчик всех других сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"Получено сообщение: {update.message.text}")
    await update.message.reply_text("Я получил твоё сообщение!")

# Регистрируем обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.ALL, echo))

# Проверочный маршрут для Render
@app.route("/", methods=["GET"])
def index():
    return "Бот работает ✅", 200

# Обработка Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        logging.info("=== ПОЛУЧЕНО ОБНОВЛЕНИЕ ОТ TELEGRAM ===")
        logging.info(data)
        update = Update.de_json(data, application.bot)

        # ВАЖНО: используем asyncio.run для запуска асинхронной обработки
        asyncio.run(application.process_update(update))

        return "ok", 200
    except Exception as e:
        logging.exception("Ошибка Webhook")
        return jsonify({"error": str(e)}), 500

# Фоновый запуск Telegram Application
async def run_telegram():
    await application.initialize()
    await application.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_telegram())
    app.run(host="0.0.0.0", port=10000)
