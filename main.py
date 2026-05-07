import os
import datetime
from datetime import time
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.getenv("TOKEN")

CHAT_IDS = os.getenv("CHAT_IDS", "")
CHAT_IDS = [int(x.strip()) for x in CHAT_IDS.split(",") if x.strip()]

VOICE_ID = "AwACAgIAAxEBAAMIaeck7mBixFtnFPvR5iPpFatiMMgAAraPAAIBoRBKIisXN4ENM5g7BA"

VIDEO_ID = "PUT_VIDEO_ID_HERE"  # вставишь после получения


# =======================
# /start
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен 👋")
    await update.message.reply_voice(voice=VOICE_ID)


# =======================
# 🔥 получение VIDEO_ID
# =======================
async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        file_id = update.message.video.file_id
        await update.message.reply_text(f"🎥 VIDEO_ID:\n{file_id}")


# =======================
# отправка видео (логика)
# =======================
async def send_video_job(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.utcnow()

    # пятница = 4
    if now.weekday() != 4:
        return

    for chat_id in CHAT_IDS:
        try:
            await context.bot.send_video(
                chat_id=chat_id,
                video=VIDEO_ID,
                caption="📹 Пятничное видео (12:00 Урал)"
            )
        except Exception as e:
            print(f"Ошибка {chat_id}: {e}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # ловим видео → выдаём file_id
    app.add_handler(MessageHandler(filters.VIDEO, get_video_id))

    job_queue = app.job_queue

    # каждый день 07:00 UTC (12:00 Урал)
    job_queue.run_daily(
        send_video_job,
        time=time(hour=7, minute=0)
    )

    print("🤖 BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
