import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

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
# /getid — ЛОВИМ ВСЁ ЧТО УГОДНО
# =======================
async def getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    print("========== NEW MESSAGE ==========")
    print(msg)
    print("================================")

    file_id = None
    file_type = "unknown"

    # voice (настоящее голосовое)
    if msg.voice:
        file_id = msg.voice.file_id
        file_type = "voice"

    # audio (пересланное / файл)
    elif msg.audio:
        file_id = msg.audio.file_id
        file_type = "audio"

    # document (файл с телефона / Telegram)
    elif msg.document:
        file_id = msg.document.file_id
        file_type = "document"

    # video
    elif msg.video:
        file_id = msg.video.file_id
        file_type = "video"

    # fallback (редкие случаи)
    elif msg.effective_attachment:
        file_id = msg.effective_attachment.file_id
        file_type = "effective_attachment"

    if file_id:
        await msg.reply_text(f"✅ TYPE: {file_type}\nfile_id:\n{file_id}")
        print("FILE_ID:", file_id, file_type)

    else:
        await msg.reply_text("❌ Файл не найден. Отправь его как файл, не текстом")
        print("NO FILE FOUND")


# =======================
# запуск
# =======================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getid", getid))

    print("🤖 BOT STARTED")

    app.run_polling()


if __name__ == "__main__":
    main()
