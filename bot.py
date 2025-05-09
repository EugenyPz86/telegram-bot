import os
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

# Обработка входящих сообщений от Telegram
@app.route('/webhook', methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# Запуск приложения
if __name__ == "__main__":
    import threading

    # Запуск Telegram application в отдельном потоке
    threading.Thread(target=application.run_polling, daemon=True).start()

    # Запуск Flask сервера (Render слушает этот порт)
    app.run(host="0.0.0.0", port=10000)