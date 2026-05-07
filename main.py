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

VIDEO_ID = "BAACAgIAAxkBAAN6afwniQABqd7swuDiWiuRqOusJaCoAAIslwACvpPpS_T8ckBYjI4FOwQ"


# =======================
# /start
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот работает 👋")
    await update.message.reply_audio(audio=VOICE_ID)


# =======================
# получить VIDEO_ID (оставляем на всякий случай)
# =======================
async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        await update.message.reply_text(
            f"🎥 VIDEO_ID:\n{update.message.video.file_id}"
        )


# =======================
# отправка видео
# =======================
async def send_video_job(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.datetime.utcnow()

    # только пятница
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
            print(f"Ошибка {chat_id}: {e}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # опционально: получать новые video_id
    app.add_handler(MessageHandler(filters.VIDEO, get_video_id))

    job_queue = app.job_queue

    # 07:00 UTC = 12:00 Урал
    job_queue.run_daily(
        send_video_job,
        time=time(hour=7, minute=0)
    )

    print("🤖 BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
