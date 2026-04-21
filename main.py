import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# сюда потом вставишь file_id
FILE_ID = "PASTE_FILE_ID_HERE"


# =======================
# /start — отправка voice
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if FILE_ID == "PASTE_FILE_ID_HERE":
        await update.message.reply_text("⚠️ Сначала получи file_id через /getid")
        return

    await update.message.reply_text("🎧 Лови голосовое")
    await update.message.reply_voice(voice=FILE_ID)


# =======================
# /getid — получение file_id
# =======================
async def getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("GETID TRIGGERED")

    msg = update.message
    file_id = None

    if msg.voice:
        file_id = msg.voice.file_id

    elif msg.audio:
        file_id = msg.audio.file_id

    elif msg.document:
        file_id = msg.document.file_id

    if file_id:
        await msg.reply_text(f"file_id:\n{file_id}")
        print("FILE_ID:", file_id)
    else:
        await msg.reply_text("📩 Отправь голосовое / аудио / файл")
        print("NO FILE FOUND")


# =======================
# запуск бота
# =======================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getid", getid))

    print("🤖 BOT STARTED")

    app.run_polling()


if __name__ == "__main__":
    main()
