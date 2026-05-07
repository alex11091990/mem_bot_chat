import os
import asyncio
import datetime
import random
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

ADMIN_ID = int(os.getenv("ADMIN_ID"))

# 🎤 голосовые
VOICE_IDS = [
    "ID_VOICE_1",
    "ID_VOICE_2",
    "ID_VOICE_3",
]

# 📹 видео
VIDEO_ID = "BAACAgIAAxkBAAN6afwniQABqd7swuDiWiuRqOusJaCoAAIslwACvpPpS_T8ckBYjI4FOwQ"

# 📸 фото
PHOTO_ID = "ID_PHOTO"

last_sent_date = None
waiting_for_file = set()


# =======================
# /start
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id == ADMIN_ID:
        keyboard = [
            [InlineKeyboardButton("👴 ПРИВЕТ ОТ ДЕДА", callback_data="voice")],
            [InlineKeyboardButton("👁 СМОТРИ ДЕДА!", callback_data="photo")],
            [InlineKeyboardButton("📹 РУЧНАЯ ОТПРАВКА", callback_data="send_video")],
            [InlineKeyboardButton("📎 УЗНАТЬ ID", callback_data="get_id")],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("👴 ПРИВЕТ ОТ ДЕДА", callback_data="voice")],
            [InlineKeyboardButton("👁 СМОТРИ ДЕД!", callback_data="photo")],
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


    # 🎤 VOICE (рандом)
    if query.data == "voice":
        try:
            voice_id = random.choice(VOICE_IDS)
            await query.message.reply_voice(voice=voice_id)
        except Exception as e:
            await query.message.reply_text(f"❌ Ошибка voice: {e}")


    # 👁 PHOTO
    elif query.data == "photo":
        try:
            await query.message.reply_photo(photo=PHOTO_ID)
        except Exception as e:
            await query.message.reply_text(f"❌ Ошибка photo: {e}")


    # 📹 видео вручную
    elif query.data == "send_video":
        if user_id != ADMIN_ID:
            return

        await query.message.reply_text("📤 Отправляю видео...")

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


    # 📎 режим получения ID
    elif query.data == "get_id":
        if user_id != ADMIN_ID:
            return

        waiting_for_file.add(user_id)
        await query.message.reply_text(
            "📎 Отправь любой файл:\nvoice / video / photo / audio / document"
        )


# =======================
# УНИВЕРСАЛЬНЫЙ FILE_ID
# =======================
async def catch_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in waiting_for_file:
        return

    msg = update.message
    file_id = None
    file_type = None

    if msg.voice:
        file_id = msg.voice.file_id
        file_type = "VOICE"

    elif msg.video:
        file_id = msg.video.file_id
        file_type = "VIDEO"

    elif msg.photo:
        file_id = msg.photo[-1].file_id
        file_type = "PHOTO"

    elif msg.audio:
        file_id = msg.audio.file_id
        file_type = "AUDIO"

    elif msg.document:
        file_id = msg.document.file_id
        file_type = "DOCUMENT"

    if file_id:
        await msg.reply_text(
            f"📦 TYPE: {file_type}\n\n📎 FILE_ID:\n`{file_id}`",
            parse_mode="Markdown"
        )
        waiting_for_file.remove(user_id)
    else:
        await msg.reply_text("❌ Не удалось определить файл")


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


async def post_init(app):
    asyncio.create_task(scheduler(app))


# =======================
# запуск
# =======================
def main():
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.ALL, catch_file))

    print("BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
