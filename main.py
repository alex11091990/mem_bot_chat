from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context):
    print("START HIT")
    await update.message.reply_text("работает")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("RUNNING BOT")
app.run_polling()
