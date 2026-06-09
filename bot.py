import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("579539")

app = ApplicationBuilder().token(os.getenv("8966882226:AAFhB8E2a6ubxg93dobkeIWVvUX0T-msBSg")).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
