from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import firebase_admin
from firebase_admin import credentials, db

# YOUR TELEGRAM BOT TOKEN
TOKEN = "8966882226:AAFhB8E2a6ubxg93dobkeIWVvUX0T-msBSg"

# FIREBASE SETUP
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://tuak-9f342-default-rtdb.firebaseio.com"
    }
)

# /start COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    ref = db.reference("TelegramBotGC")

    ref.set({
        "message": "test ok"
    })

    await update.message.reply_text("Saved to Firebase")

# START BOT
def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
