from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import os
import json
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")  # Better to use env var too

# Firebase Config - Set these on Railway
DATABASE_URL = os.getenv("FIREBASE_DB_URL")      # e.g. https://your-project-id-default-rtdb.firebaseio.com
DB_SECRET = os.getenv("FIREBASE_SECRET")         # Database secret (see below)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    data = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "timestamp": datetime.utcnow().isoformat(),
        "message": "579539"
    }
    
    try:
        # Send to Firebase
        url = f"{DATABASE_URL}/starts.json?auth={DB_SECRET}"
        response = requests.post(url, json=data)
        
        if response.ok:
            print("✅ Data saved to Firebase")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    await update.message.reply_text("579539")

# Main
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot running...")
app.run_polling()
