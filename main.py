import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

VOICE_URL = "https://drive.google.com/uc?export=download&id=1bofSKvmZW90mPwPbHSsEsGhbwGaFeYYo"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎧 Лови голосовое")

    response = requests.get(VOICE_URL)

    with open("voice.ogg", "wb") as f:
        f.write(response.content)

    with open("voice.ogg", "rb") as f:
        await update.message.reply_voice(voice=f)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("🤖 BOT STARTED")

    app.run_polling()


if __name__ == "__main__":
    main()
