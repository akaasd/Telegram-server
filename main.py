from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import firebase_admin
from firebase_admin import credentials, db
import json
import os

TOKEN = "8966882226:AAFhB8E2a6ubxg93dobkeIWVvUX0T-msBSg"

# ====================== FIREBASE SETUP ======================
# Load credentials from Railway Environment Variable
firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS")
if not firebase_creds_json:
    raise ValueError("FIREBASE_CREDENTIALS environment variable is missing!")

cred = credentials.Certificate(json.loads(firebase_creds_json))

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tuak-9f342-default-rtdb.firebaseio.com'   # ← CHANGE THIS
})

# ===========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    data = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "timestamp": str(update.message.date),
        "message": "579539"
    }
    
    try:
        ref = db.reference('starts')   # You can change 'starts' to anything
        ref.push(data)
        print(f"✅ Saved to Firebase: {user.id}")
    except Exception as e:
        print(f"❌ Firebase Error: {e}")
    
    await update.message.reply_text("579539")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot is running...")
app.run_polling()
