import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
CHAT_ID_1 = os.getenv("CHAT_ID_1")
CHAT_ID_2 = os.getenv("CHAT_ID_2")

FILE_ID = "AwACAgIAAxkBAAMIaeck7mBixFtnFPvR5iPpFatiMMgAAraPAAIBoRBKIisXN4ENM5g7BA"


# =======================
# /start — личка
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет от деда:")
    await update.message.reply_voice(voice=FILE_ID)


# =======================
# рассылка в чаты
# =======================
async def send_to_chats(context: ContextTypes.DEFAULT_TYPE):
    try:
        for chat_id in [CHAT_ID_1, CHAT_ID_2]:
            await context.bot.send_message(chat_id=chat_id, text="Всех с пятницей!")
            await context.bot.send_voice(chat_id=chat_id, voice=FILE_ID)

        print("✅ Рассылка отправлена")

    except Exception as e:
        print("❌ Ошибка рассылки:", e)


# =======================
# запуск
# =======================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # 🔥 каждые 5 минут (для теста)
    app.job_queue.run_repeating(send_to_chats, interval=300, first=10)

    print("🤖 BOT STARTED")

    app.run_polling()


if __name__ == "__main__":
    main()
