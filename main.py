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

# 🎤 голосовые (3 штуки)
VOICE_IDS = [
    "AwACAgIAAxkDAAN5afwl9MjEATd7mAOB0mgis2NGzUgAAraPAAIBoRBKIisXN4ENM5g7BA",
    "AwACAgIAAxkBAAO_afw_DKWypppxjJi-A7fH2eJMi1kAAg2RAAL-EPlIcTuAC6lc7HA7BA",
    "AwACAgIAAxkBAAPCafw_aDN0oh3s-bNFFhGH9v7HC4cAAtWVAAJRo-lLHrC_1mK96Xw7BA",
]

# 📹 видео
VIDEO_ID = "BAACAgIAAxkBAAN6afwniQABqd7swuDiWiuRqOusJaCoAAIslwACvpPpS_T8ckBYjI4FOwQ"

# 📸 фото
PHOTO_ID = "PHOTO_ID"

last_sent_date = None
waiting_for_file = set()


# =======================
# START
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    keyboard = [
        [InlineKeyboardButton("👴 ПРИВЕТ ОТ ДЕДА", callback_data="voice")],
        [InlineKeyboardButton("👁 СМОТРИ ДЕД!", callback_data="photo")],
    ]

    if user_id == ADMIN_ID:
        keyboard.append(
            [InlineKeyboardButton("📹 РУЧНАЯ ОТПРАВКА", callback_data="send_video")]
        )
        keyboard.append(
            [InlineKeyboardButton("📎 УЗНАТЬ ID", callback_data="get_id")]
        )

    await update.message.reply_text(
        "Выбери действие:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =======================
# КНОПКИ
# =======================
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id


    # 🎤 VOICE (рандом)
    if query.data == "voice":
        try:
            voice = random.choice(VOICE_IDS)
            await query.message.reply_voice(voice=voice)
        except Exception as e:
            await query.message.reply_text(f"❌ voice error: {e}")


    # 👁 PHOTO
    elif query.data == "photo":
        try:
            await query.message.reply_photo(photo=PHOTO_ID)
        except Exception as e:
            await query.message.reply_text(f"❌ photo error: {e}")


    # 📹 SEND VIDEO
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

        await query.message.reply_text("✅ Готово")


    # 📎 GET ID MODE
    elif query.data == "get_id":
        if user_id != ADMIN_ID:
            return

        waiting_for_file.add(user_id)
        await query.message.reply_text("📎 Отправь любой файл (voice/video/photo/audio/document)")


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
            f"📦 TYPE: {file_type}\n\n📎 FILE_ID:\n{file_id}"
        )
        waiting_for_file.remove(user_id)
    else:
        await msg.reply_text("❌ Не удалось определить файл")


# =======================
# АВТО РАССЫЛКА (пятница)
# =======================
async def scheduler(app):
    global last_sent_date

    while True:
        try:
            now = datetime.datetime.utcnow()

            if now.weekday() == 4 and now.hour == 7 and now.minute == 0:
                today = now.date()

                if last_sent_date != today:
                    print("📹 AUTO SEND")

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
# MAIN
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
