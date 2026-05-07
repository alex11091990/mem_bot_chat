import os
import asyncio
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

CHAT_IDS = os.getenv("CHAT_IDS", "")
CHAT_IDS = [int(x.strip()) for x in CHAT_IDS.split(",") if x.strip()]

# ✅ твой рабочий file_id (voice)
FILE_ID = "AwACAgIAAxkBAAMIaeck7mBixFtnFPvR5iPpFatiMMgAAraPAAIBoRBKIisXN4ENM5g7BA"

VIDEO_ID = "BAACAgIAAxkBAAN6afwniQABqd7swuDiWiuRqOusJaCoAAIslwACvpPpS_T8ckBYjI4FOwQ"

last_sent_date = None


# =======================
# /start (как раньше)
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("Привет от деда:")
        await update.message.reply_voice(voice=FILE_ID)

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")
        print("ERROR:", e)


# =======================
# авто-рассылка
# =======================
async def scheduler(app):
    global last_sent_date

    while True:
        try:
            now = datetime.datetime.utcnow()

            # пятница 07:00 UTC = 12:00 Урал
            if now.weekday() == 4 and now.hour == 7:
                today = now.date()

                if last_sent_date != today:
                    print("📹 Отправка видео...")

                    for chat_id in CHAT_IDS:
                        try:
                            await app.bot.send_video(
                                chat_id=chat_id,
                                video=VIDEO_ID,
                                caption="📹 ВСЕХ С ПЯТНИЦЕЙ!"
                            )
                        except Exception as e:
                            print(f"ERROR {chat_id}: {e}")

                    last_sent_date = today

        except Exception as e:
            print("SCHEDULER ERROR:", e)

        await asyncio.sleep(30)


# =======================
# запуск фонового цикла
# =======================
async def post_init(app):
    asyncio.create_task(scheduler(app))


def main():
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))

    print("BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
