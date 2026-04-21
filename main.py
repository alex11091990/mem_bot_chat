import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")


# 👉 сюда потом вставишь file_id
FILE_ID = "PASTE_FILE_ID_HERE"


# /start — проверка отправки голосового
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if FILE_ID == "PASTE_FILE_ID_HERE":
        await update.message.reply_text("⚠️ Сначала добавь file_id через /getid")
        return

    await update.message.reply_text("🎧 Лови голосовое")
    await update.message.reply_voice(voice=FILE_ID)


# /getid — получить file_id голосового
async def getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice

    if voice:
        file_id = voice.file_id
        await update.message.reply_text(f"file_id:\n{file_id}")
        print("FILE_ID:", file_id)
    else:
        await update.message.reply_text("📩 Пришли голосовое сообщение")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getid", getid))

    print("🤖 BOT STARTED")

    app.run_polling()


if __name__ == "__main__":
    main()
