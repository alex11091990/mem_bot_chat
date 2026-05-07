import os
import asyncio
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

CHAT_IDS = os.getenv("CHAT_IDS", "")
CHAT_IDS = [int(x.strip()) for x in CHAT_IDS.split(",") if x.strip()]

FILE_ID_1 = "AwACAgIAAxEBAAMIaeck7mBixFtnFPvR5iPpFatiMMgAAraPAAIBoRBKIisXN4ENM5g7BA"

FILE_ID_2 = "BAACAgIAAxkBAAN6afwniQABqd7swuDiWiuRqOusJaCoAAIslwACvpPpS_T8ckBYjI4FOwQ"

# чтобы не отправляло 100 раз
last_sent_date = None


# =======================
# /start
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет от деда:")

    await.update.message.reply_voice(voice=FILE_ID_1)


# =======================
# авто-рассылка (без JobQueue)
# =======================
async def scheduler(app):
    global last_sent_date

    while True:
        now = datetime.datetime.utcnow()

        # пятница = 4
        if now.weekday() == 4 and now.hour == 7:
            today = now.date()

            # защита от повторной отправки
            if last_sent_date != today:
                print("📹 Отправка видео...")

                for chat_id in CHAT_IDS:
                    try:
                        await app.bot.send_video(
                            chat_id=chat_id,
                            video=FILE_ID_2,
                            caption="📹 ВСЕХ С ПЯТНИЦЕЙ!"
                        )
                    except Exception as e:
                        print(f"ERROR {chat_id}: {e}")

                last_sent_date = today

        # проверка раз в 30 секунд
        await asyncio.sleep(30)


# =======================
# запуск
# =======================
async def post_init(app):
    # запускаем фоновый цикл
    asyncio.create_task(scheduler(app))


def main():
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))

    print("BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
