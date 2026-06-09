from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import os
from datetime import datetime
import random

TOKEN = os.getenv("TELEGRAM_TOKEN")
DATABASE_URL = os.getenv("FIREBASE_DB_URL")
DB_SECRET = os.getenv("FIREBASE_SECRET")

PATH = "TelegramBotGC"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    now = datetime.utcnow()
    
    # Generate new 6-digit code
    new_code = f"{random.randint(100000, 999999)}"
    
    # Prepare data
    save_data = {
        "giftcode": new_code,
        "timestamp": int(now.timestamp() * 1000)   # milliseconds like JavaScript Date.now()
    }
    
    try:
        url = f"{DATABASE_URL}/{PATH}.json?auth={DB_SECRET}"
        response = requests.put(url, json=save_data, timeout=10)
        
        if response.ok:
            print(f"✅ New code generated and saved: {new_code}")
            await update.message.reply_text(new_code)
        else:
            print(f"❌ Firebase save failed: {response.text}")
            await update.message.reply_text(new_code)  # Still send code
            
    except Exception as e:
        print(f"❌ Error: {e}")
        await update.message.reply_text(new_code)  # Fallback: still send code

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot running - New giftcode every /start")
app.run_polling()
