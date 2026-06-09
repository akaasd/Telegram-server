import random
import time

import firebase_admin
from firebase_admin import credentials, db

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# BOT TOKEN
TOKEN = "8966882226:AAFhB8E2a6ubxg93dobkeIWVvUX0T-msBSg"

# FIREBASE
cred = credentials.Certificate("serviceAccountKey.json")

firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://tuak-9f342-default-rtdb.firebaseio.com"
    }
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    ref = db.reference("TelegramBotGC")
    data = ref.get()

    current_timestamp = int(time.time() * 1000)

    if data is None:
        giftcode = "357327"

        ref.set({
            "giftcode": giftcode,
            "timestamp": current_timestamp
        })

        await update.message.reply_text(giftcode)
        return

    saved_timestamp = int(data.get("timestamp", 0))
    saved_giftcode = str(data.get("giftcode", "357327"))

    twelve_hours = 12 * 60 * 60 * 1000

    if (current_timestamp - saved_timestamp) >= twelve_hours:

        new_giftcode = str(random.randint(100000, 999999))

        ref.set({
            "giftcode": new_giftcode,
            "timestamp": current_timestamp
        })

        await update.message.reply_text(new_giftcode)

    else:
        await update.message.reply_text(saved_giftcode)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
