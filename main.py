import asyncio
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

VOICE_URL = "https://drive.google.com/file/d/1bofSKvmZW90mPwPbHSsEsGhbwGaFeYYo/view?usp=sharing"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🎧 Лови голосовое")

        response = requests.get(VOICE_URL)

        with open("voice.ogg", "wb") as f:
            f.write(response.content)

        with open("voice.ogg", "rb") as f:
            await update.message.reply_voice(voice=f)

        print("✅ Отправлено")

    except Exception as e:
        print("❌ Ошибка:", e)


async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("🤖 Бот запущен...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
