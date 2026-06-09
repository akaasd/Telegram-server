from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import os
from datetime import datetime, timedelta
import random

TOKEN = os.getenv("TELEGRAM_TOKEN")
DATABASE_URL = os.getenv("FIREBASE_DB_URL")
DB_SECRET = os.getenv("FIREBASE_SECRET")

PATH = "TelegramBotGC"   # The path you want

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    now = datetime.utcnow()

    try:
        # 1. Get current data from Firebase
        get_url = f"{DATABASE_URL}/{PATH}.json?auth={DB_SECRET}"
        response = requests.get(get_url)
        
        data = response.json() if response.ok and response.json() else {}
        
        stored_code = data.get("giftcode")
        stored_timestamp = data.get("timestamp")
        
        should_generate_new = True
        
        if stored_timestamp:
            # Convert timestamp to datetime
            last_time = datetime.fromtimestamp(stored_timestamp / 1000)  # Firebase often uses ms
            hours_diff = (now - last_time).total_seconds() / 3600
            
            if hours_diff < 12:
                should_generate_new = False
        
        if should_generate_new or not stored_code:
            # Generate new 6-digit code
            new_code = f"{random.randint(100000, 999999)}"
            
            # Save to Firebase
            save_data = {
                "giftcode": new_code,
                "timestamp": int(now.timestamp() * 1000)  # milliseconds
            }
            
            put_url = f"{DATABASE_URL}/{PATH}.json?auth={DB_SECRET}"
            requests.put(put_url, json=save_data)
            
            await update.message.reply_text(new_code)
            print(f"✅ New giftcode generated: {new_code} for user {user.id}")
        else:
            # Send existing code
            await update.message.reply_text(stored_code)
            print(f"✅ Sent existing code: {stored_code} to user {user.id}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        # Fallback: generate new code if something fails
        new_code = f"{random.randint(100000, 999999)}"
        await update.message.reply_text(new_code)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot is running with daily giftcode logic...")
app.run_polling()
