import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
application = ApplicationBuilder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я теперь работаю на Render через Webhook 😊")

application.add_handler(CommandHandler("start", start))

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Фоновый запуск Telegram-приложения
async def run_telegram():
    await application.initialize()
    await application.bot.set_webhook("https://telegram-bot-hxh5.onrender.com/webhook")
    await application.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_telegram())  # ← ключевой момент
    app.run(host="0.0.0.0", port=10000)