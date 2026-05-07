import os
import asyncio
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")

CHAT_IDS = os.getenv("CHAT_IDS", "")
CHAT_IDS = [int(x.strip()) for x in CHAT_IDS.split(",") if x.strip()]

FILE_ID = "CQACAgIAAxkBAAOxafw7W0OLl5ZkT62bnFFBfVGnlX8AAuWXAAK-k-lLUw32eMQVcLg7BA"
VIDEO_ID = "BAACAgIAAxkBAAN6afwniQABqd7swuDiWiuRqOusJaCoAAIslwACvpPpS_T8ckBYjI4FOwQ"

last_sent_date = None

# режим ожидания файла для получения ID
waiting_for_file = set()


# =======================
# /start меню
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👴 ПРИВЕТ ОТ ДЕДА", callback_data="voice")],
        [InlineKeyboardButton("📤 РУЧНАЯ ОТПРАВКА", callback_data="send_video")],
        [InlineKeyboardButton("📎 УЗНАТЬ ID", callback_data="get_id")]
    ]

    await update.message.reply_text(
        "Выбери действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =======================
# кнопки
# =======================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    # 👴 voice
    if query.data == "voice":
        try:
            try:
                await query.message.reply_voice(voice=FILE_ID)
            except Exception:
                try:
                    await query.message.reply_audio(audio=FILE_ID)
                except Exception:
                    await query.message.reply_document(document=FILE_ID)
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

    # 📎 get file id
    elif query.data == "get_id":
        waiting_for_file.add(user_id)
        await query.message.reply_text(
            "📎 Отправь мне любой файл:\nvoice / video / audio\n\nЯ верну тебе FILE_ID"
        )


# =======================
# ловим файлы
# =======================
async def catch_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in waiting_for_file:
        return

    msg = update.message

    file_id = None

    if msg.voice:
        file_id = msg.voice.file_id
    elif msg.audio:
        file_id = msg.audio.file_id
    elif msg.video:
        file_id = msg.video.file_id
    elif msg.document:
        file_id = msg.document.file_id

    if file_id:
        await msg.reply_text(f"📎 FILE_ID:\n{file_id}")
        waiting_for_file.remove(user_id)
    else:
        await msg.reply_text("❌ Не смог получить file_id")


# =======================
# scheduler (пятница)
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


async def post_init(app):
    asyncio.create_task(scheduler(app))


# =======================
# запуск
# =======================
def main():
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # ловим файлы для /get_id
    app.add_handler(MessageHandler(filters.VOICE | filters.VIDEO | filters.AUDIO | filters.Document.ALL, catch_file))

    print("BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
