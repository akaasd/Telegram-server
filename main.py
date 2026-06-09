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
    now_ms = int(datetime.utcnow().timestamp() * 1000)
    
    try:
        # Get data from Firebase
        get_url = f"{DATABASE_URL}/{PATH}.json?auth={DB_SECRET}"
        response = requests.get(get_url, timeout=10)
        data = response.json() if response.ok else {}
        
        stored_giftcode = data.get("giftcode")
        stored_timestamp = data.get("timestamp")
        
        generate_new = True
        
        if stored_timestamp and isinstance(stored_timestamp, (int, float)):
            time_diff_ms = now_ms - stored_timestamp
            time_diff_minutes = time_diff_ms / (1000 * 60)
            
            if time_diff_minutes <= 1:
                generate_new = False
        
        if generate_new or not stored_giftcode:
            new_code = f"{random.randint(100000, 999999)}"
            
            save_data = {
                "giftcode": new_code,
                "timestamp": now_ms
            }
            
            put_url = f"{DATABASE_URL}/{PATH}.json?auth={DB_SECRET}"
            requests.put(put_url, json=save_data, timeout=10)
            
            giftcode = new_code
            print(f"✅ New code generated: {new_code}")
        else:
            giftcode = stored_giftcode
            print(f"✅ Sent existing code: {giftcode}")
        
        # Send beautiful formatted message with BOLD code
        message = f"""🎁 BASF Gift Code Available!
Your BASF Gift Code is:
**{giftcode}**

Use this code to access your available gift. We hope you enjoy it!
⏰ Please note: Gift codes reset at 12:00 AM tonight. Be sure to check back tomorrow for a new BASF Gift Code."""

        await update.message.reply_text(message, parse_mode="MarkdownV2")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        # Fallback message
        fallback_code = f"{random.randint(100000, 999999)}"
        message = f"""🎁 BASF Gift Code Available!
Your BASF Gift Code is:
**{fallback_code}**

Use this code to access your available gift. We hope you enjoy it!
⏰ Please note: Gift codes reset at 12:00 AM tonight. Be sure to check back tomorrow for a new BASF Gift Code."""
        await update.message.reply_text(message, parse_mode="MarkdownV2")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot running with styled message...")
app.run_polling()
