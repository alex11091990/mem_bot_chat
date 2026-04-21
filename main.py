import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")


# =======================
# авто-ловим ВСЕ файлы
# =======================
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    file_id = None
    file_type = None

    if msg.voice:
        file_id = msg.voice.file_id
        file_type = "voice"

    elif msg.audio:
        file_id = msg.audio.file_id
        file_type = "audio"

    elif msg.document:
        file_id = msg.document.file_id
        file_type = "document"

    elif msg.video:
        file_id = msg.video.file_id
        file_type = "video"

    elif msg.video_note:
        file_id = msg.video_note.file_id
        file_type = "video_note"

    if file_id:
        await msg.reply_text(
            f"✅ TYPE: {file_type}\nfile_id:\n{file_id}"
        )
        print("FILE_ID:", file_id, file_type)

    else:
        await msg.reply_text("📩 Отправь файл (voice/audio/document/video)")


# =======================
# запуск
# =======================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # ловим ВСЕ медиа сообщения
    app.add_handler(MessageHandler(filters.ALL, handle_file))

    print("🤖 BOT STARTED")

    app.run_polling()


if __name__ == "__main__":
    main()
