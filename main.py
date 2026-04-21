import os
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
CHAT_ID_1 = os.getenv("CHAT_ID_1")
CHAT_ID_2 = os.getenv("CHAT_ID_2")

# голосовое по file_id (для /start)
VOICE_FILE_ID = "AwACAgIAAxkBAAMIaeck7mBixFtnFPvR5iPpFatiMMgAAraPAAIBoRBKIisXN4ENM5g7BA"

# файл с Google Drive
VOICE_URL = "https://drive.google.com/uc?export=download&id=15uMBtP73WGYjSlQpbCByqiX6k52hyKwQ"


# =======================
# /start — ответ пользователю
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет от деда: ")

    await update.message.reply_voice(voice=VOICE_FILE_ID)


# =======================
# рассылка в чаты
# =======================
async def send_to_chats(context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(VOICE_URL)

        with open("voice.ogg", "wb") as f:
            f.write(response.content)

        for chat_id in [CHAT_ID_1, CHAT_ID_2]:
            with open("voice.ogg", "rb") as f:
                await context.bot.send_voice(chat_id=chat_id, voice=f)

        print("✅ Рассылка отправлена")

    except Exception as e:
        print("❌ Ошибка рассылки:", e)


# =======================
# запуск бота
# =======================
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("🤖 BOT STARTED")

    # фоновая задача (если нужно по cron)
    # await send_to_chats(app.bot)

    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
