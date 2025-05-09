import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# Обработчик /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я теперь работаю на Render через Webhook 😊")

application.add_handler(CommandHandler("start", start))

# Принимаем сообщения от Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Основная асинхронная функция
async def main():
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    # Flask запускается в отдельном потоке
    from threading import Thread
    Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()
    await application.updater.wait()

if __name__ == "__main__":
    asyncio.run(main())