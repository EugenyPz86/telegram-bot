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
logger = logging.getLogger(__name__)

# Flask-приложение
app = Flask(__name__)

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в переменных окружения!")

# Инициализируем Telegram Application
application = ApplicationBuilder().token(TOKEN).build()

# Обработчики
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я работаю через Webhook на Render 🎉")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Получено сообщение: {update.message.text}")
    await update.message.reply_text("Я получил твоё сообщение!")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.ALL, echo))

# Проверочный маршрут
@app.route("/", methods=["GET"])
def index():
    return "Бот работает ✅", 200

# Webhook-обработка
@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        data = request.get_json(force=True)
        logger.info("=== ПОЛУЧЕНО ОБНОВЛЕНИЕ ОТ TELEGRAM ===")
        logger.info(data)

        update = Update.de_json(data, application.bot)
        await application.process_update(update)

        return "ok", 200
    except Exception as e:
        logger.exception("Ошибка Webhook")
        return jsonify({"error": str(e)}), 500

# Асинхронный запуск Telegram Application
async def run_bot():
    await application.initialize()
    await application.start()
    logger.info("Бот запущен ✅")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
    app.run(host="0.0.0.0", port=10000)