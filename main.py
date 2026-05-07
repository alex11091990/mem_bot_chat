import os
import asyncio
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

TOKEN = os.getenv("TOKEN")

CHAT_IDS = os.getenv("CHAT_IDS", "")
CHAT_IDS = [int(x.strip()) for x in CHAT_IDS.split(",") if x.strip()]

FILE_ID = "AwACAgIAAxEBAAMIaeck7mBixFtnFPvR5iPpFatiMMgAAraPAAIBoRBKIisXN4ENM5g7BA"

VIDEO_ID = "BAACAgIAAxkBAAN6afwniQABqd7swuDiWiuRqOusJaCoAAIslwACvpPpS_T8ckBYjI4FOwQ"

last_sent_date = None


# =======================
# /start меню
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👴 ПРИВЕТ ОТ ДЕДА", callback_data="voice")],
        [InlineKeyboardButton("📤 РУЧНАЯ ОТПРАВКА", callback_data="send_video")]
    ]

    await update.message.reply_text(
        "Выбери действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =======================
# обработка кнопок
# =======================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # 👴 voice
    if query.data == "voice":
        try:
            await query.message.reply_audio(audio=FILE_ID)
        except Exception as e:
            await query.message.reply_text(f"❌ Ошибка voice: {e}")

    # 📤 video
    elif query.data == "send_video":
        await query.message.reply_text("📤 Отправляю видео во все чаты...")

        for chat_id in CHAT_IDS:
            try:
                await context.bot.send_video(
                    chat_id=chat_id,
                    video=VIDEO_ID,
                    caption="📹 РУЧНАЯ ОТПРАВКА"
                )
            except Exception as e:
                print(f"ERROR {chat_id}: {e}")

        await query.message.reply_text("✅ Готово!")


# =======================
# авто-рассылка (пятница)
# =======================
async def scheduler(app):
    global last_sent_date

    while True:
        try:
            now = datetime.datetime.utcnow()

            if now.weekday() == 4 and now.hour == 7 and now.minute == 0:
                today = now.date()

                if last_sent_date != today:
                    print("📹 AUTO SEND...")

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

        await asyncio.sleep(10)


# =======================
# запуск
# =======================
async def post_init(app):
    asyncio.create_task(scheduler(app))


def main():
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
