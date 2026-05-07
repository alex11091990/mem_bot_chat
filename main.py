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

# =======================
# РАБОЧИЙ VOICE (как у тебя был)
# =======================
FILE_ID = "AwACAgIAAxkBAAMIaeck7mBixFtnFPvR5iPpFatiMMgAAraPAAIBoRBKIisXN4ENM5g7BA"

# видео
VIDEO_ID = "BAACAgIAAxkBAAN6afwniQABqd7swuDiWiuRqOusJaCoAAIslwACvpPpS_T8ckBYjI4FOwQ"


# =======================
# /start — как в рабочей версии
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("Привет от деда:")
        await update.message.reply_voice(voice=FILE_ID)

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")
        print("ERROR:", e)


# =======================
# видео ID (оставляем)
# =======================
async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        await update.message.reply_text(update.message.video.file_id)


# =======================
# отправка видео
# =======================
async def send_video_job(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.utcnow()

    # пятница
    if now.weekday() != 4:
        return

    for chat_id in CHAT_IDS:
        try:
            await context.bot.send_video(
                chat_id=chat_id,
                video=VIDEO_ID,
                caption="📹 ВСЕХ С ПЯТНИЦЕЙ!"
            )
        except Exception as e:
            print("ERROR:", e)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, get_video_id))

    job_queue = app.job_queue

    # ⚠️ ПРОСТО И СТАБИЛЬНО (как ты хотел)
    job_queue.run_daily(
        send_video_job,
        time=time(hour=7, minute=0)
    )

    print("BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
