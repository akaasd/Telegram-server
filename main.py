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
    now_ms = int(datetime.utcnow().timestamp() * 1000)   # Current time in milliseconds
    
    try:
        # Step 1: Get current data from Firebase
        get_url = f"{DATABASE_URL}/{PATH}.json?auth={DB_SECRET}"
        response = requests.get(get_url, timeout=10)
        
        data = response.json() if response.ok else {}
        
        stored_giftcode = data.get("giftcode")
        stored_timestamp = data.get("timestamp")
        
        # Step 2: Check if we need to generate new code
        generate_new = True
        
        if stored_timestamp and isinstance(stored_timestamp, (int, float)):
            time_diff_ms = now_ms - stored_timestamp
            time_diff_minutes = time_diff_ms / (1000 * 60)
            
            if time_diff_minutes <= 1:
                generate_new = False
        
        if generate_new or not stored_giftcode:
            # Generate new 6-digit code
            new_code = f"{random.randint(100000, 999999)}"
            
            save_data = {
                "giftcode": new_code,
                "timestamp": now_ms
            }
            
            # Save to Firebase
            put_url = f"{DATABASE_URL}/{PATH}.json?auth={DB_SECRET}"
            requests.put(put_url, json=save_data, timeout=10)
            
            await update.message.reply_text(new_code)
            print(f"✅ New code generated: {new_code} for user {user.id}")
        else:
            # Send existing code (within 1 minute)
            await update.message.reply_text(stored_giftcode)
            print(f"✅ Sent existing code: {stored_giftcode} to user {user.id}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        # Fallback: Generate and send new code if anything fails
        new_code = f"{random.randint(100000, 999999)}"
        await update.message.reply_text(new_code)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot running - 1 minute giftcode cooldown")
app.run_polling()
