import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я теперь работаю на Render через Webhook 😊")

application.add_handler(CommandHandler("start", start))

# Webhook: получает сообщения от Telegram
@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Асинхронный запуск Telegram-приложения
async def run():
    await application.initialize()
    await application.start()
    # Не запускаем polling — всё работает через Webhook

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run())
    app.run(host="0.0.0.0", port=10000)