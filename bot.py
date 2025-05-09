import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Переменные окружения
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = "https://telegram-bot-hxh5.onrender.com/webhook"

# Flask-приложение
app = Flask(__name__)

# Telegram-приложение
application = ApplicationBuilder().token(TOKEN).build()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я теперь работаю на Render через Webhook 😊")

application.add_handler(CommandHandler("start", start))

# Webhook-эндпоинт
@app.route('/webhook', methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Основной запуск
async def main():
    await application.initialize()
    await application.bot.set_webhook(WEBHOOK_URL)
    await application.start()
    print("Бот запущен и webhook установлен")

if __name__ == "__main__":
    asyncio.get_event_loop().create_task(main())
    app.run(host="0.0.0.0", port=10000)
