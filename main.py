import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# твой file_id
FILE_ID = "AwACAgIAAxkBAAMIaeck7mBixFtnFPvR5iPpFatiMMgAAraPAAIBoRBKIisXN4ENM5g7BA"


# =======================
# /start — отправка voice
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("Привет от деда:")
        await update.message.reply_voice(voice=FILE_ID)

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")
        print("ERROR:", e)


# =======================
# запуск
# =======================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("🤖 BOT STARTED")

    app.run_polling()


if __name__ == "__main__":
    main()
