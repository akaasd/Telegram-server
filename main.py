import random
import time
import requests

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8966882226:AAFhB8E2a6ubxg93dobkeIWVvUX0T-msBSg"

DATABASE_URL = "https://tuak-9f342-default-rtdb.firebaseio.com/TelegramBotGC.json"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    current_timestamp = int(time.time() * 1000)

    try:
        response = requests.get(DATABASE_URL)
        data = response.json()

        if not data:
            giftcode = "357327"

            requests.put(DATABASE_URL, json={
                "giftcode": giftcode,
                "timestamp": current_timestamp
            })

            await update.message.reply_text(giftcode)
            return

        saved_timestamp = int(data.get("timestamp", 0))
        saved_giftcode = str(data.get("giftcode", "357327"))

        twelve_hours = 12 * 60 * 60 * 1000

        if current_timestamp - saved_timestamp >= twelve_hours:

            new_code = str(random.randint(100000, 999999))

            requests.put(DATABASE_URL, json={
                "giftcode": new_code,
                "timestamp": current_timestamp
            })

            await update.message.reply_text(new_code)

        else:
            await update.message.reply_text(saved_giftcode)

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

app.run_polling()
