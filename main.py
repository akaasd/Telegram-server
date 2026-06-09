async def start(update, context):

    ref = db.reference("TelegramBotGC")

    ref.set({
        "message": "test ok"
    })

    await update.message.reply_text("Saved to Firebase")
