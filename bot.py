from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Вставь сюда свой токен от BotFather
TOKEN = "8078963182:AAEshVYNwsNPbKTZXaxeWv8ZCeZ7XZIqnS4"

# Главное меню
keyboard = [
    ["🔹 Как это работает"],
    ["📩 Стать партнёром", "📦 Получить материалы"],
    ["🧁 Заказать дегустацию", "📋 FAQ и поддержка"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я — бот партнёрской программы Desert.O'clock.\n\nВыбери, с чего начнём 👇",
        reply_markup=reply_markup
    )

# Обработка нажатий на кнопки (текстовые сообщения)
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🔹 Как это работает":
        await update.message.reply_text(
            "📌 Как это работает:\n\n"
            "1. Ты находишь B2B-клиента (кафе, доставка)\n"
            "2. Рассказываешь о продукте и условиях\n"
            "3. Клиент готов работать\n"
            "4. Мы берём его в работу, а ты получаешь выплаты каждый месяц\n\n"
            "💸 Бронза: до 500 моти – 10₽\n"
            "🥈 Серебро: 501–2000 моти – 12₽\n"
            "🥇 Золото: от 2001 моти – 15₽"
        )

    elif text == "📩 Стать партнёром":
        await update.message.reply_text(
            "📩 Заполни короткую анкету:\n"
            "🔗 https://forms.gle/ТВОЯ_ССЫЛКА"
        )

    elif text == "📦 Получить материалы":
        await update.message.reply_text(
            "📦 Полезные материалы:\n\n"
            "📘 Инструкция: [ссылка]\n"
            "📄 Прайс: [ссылка]\n"
            "🎯 Презентация: [ссылка]"
        )

    elif text == "🧁 Заказать дегустацию":
        await update.message.reply_text(
            "🧁 Хочешь предложить клиенту дегустацию?\n\n"
            "Мы отправляем наборы по оптовой цене, по предоплате.\n"
            "🔗 Заявка: https://forms.gle/ТВОЯ_ССЫЛКА"
        )

    elif text == "📋 FAQ и поддержка":
        await update.message.reply_text(
            "📋 Часто задаваемые вопросы:\n\n"
            "— Как стать самозанятым?\n"
            "— Как выставить чек?\n"
            "— Когда приходят выплаты?\n\n"
            "📬 Свяжись с нами: @ТВОЙ_ЮЗЕРНЕЙМ"
        )

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
app.run_polling()