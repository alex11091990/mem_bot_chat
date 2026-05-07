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

# 👑 ADMIN ID берём из Railway ENV
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# 📎 медиа
FILE_ID = "AwACAgIAAxkDAAN5afwl9MjEATd7mAOB0mgis2NGzUgAAraPAAIBoRBKIisXN4ENM5g7BA"
VIDEO_ID = "BAACAgIAAxkBAAN6afwniQABqd7swuDiWiuRqOusJaCoAAIslwACvpPpS_T8ckBYjI4FOwQ"

last_sent_date = None
waiting_for_file = set()


# =======================
# /start (разные меню)
# =======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id == ADMIN_ID:
        keyboard = [
            [InlineKeyboardButton("👴 ПРИВЕТ ОТ ДЕДА", callback_data="voice")],
            [InlineKeyboardButton("📹 РУЧНАЯ ОТПРАВКА", callback_data="send_video")],
            [InlineKeyboardButton("📎 УЗНАТЬ ID", callback_data="get_id")],
            [InlineKeyboardButton("🛠 ПАНЕЛЬ", callback_data="admin_panel")]
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("👴 ПРИВЕТ ОТ ДЕДА", callback_data="voice")]
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


    # 👴 VOICE
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


    # 📹 VIDEO (ручная)
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
        await query.message.reply_text("📎 Отправь файл (voice/video/audio)")


    # 🛠 админ панель
    elif query.data == "admin_panel":
        if user_id != ADMIN_ID:
            return

        keyboard = [
            [InlineKeyboardButton("👴 Голос", callback_data="admin_voice")],
            [InlineKeyboardButton("📹 Видео", callback_data="admin_video")],
            [InlineKeyboardButton("📊 Статус", callback_data="status")]
        ]

        await query.message.reply_text(
            "🛠 Админ-панель:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # 👑 admin voice
    elif query.data == "admin_voice":
        if user_id != ADMIN_ID:
            return

        await query.message.reply_voice(voice=FILE_ID)


    # 👑 admin video
    elif query.data == "admin_video":
        if user_id != ADMIN_ID:
            return

        for chat_id in CHAT_IDS:
            await context.bot.send_video(
                chat_id=chat_id,
                video=VIDEO_ID,
                caption="📹 АДМИН ОТПРАВКА"
            )

        await query.message.reply_text("✅ Отправлено")


    # 📊 статус
    elif query.data == "status":
        if user_id != ADMIN_ID:
            return

        await query.message.reply_text(
            f"🤖 BOT ACTIVE\n"
            f"📡 Chats: {len(CHAT_IDS)}\n"
            f"👑 Admin: OK"
        )


# =======================
# получение file_id
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
        await msg.reply_text("❌ Не удалось получить ID")


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
    app.add_handler(MessageHandler(filters.VOICE | filters.VIDEO | filters.AUDIO | filters.Document.ALL, catch_file))

    print("BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
