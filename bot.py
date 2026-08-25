import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]

KEYWORDS = [
    "dm",
    "message me"
]


async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post

    if not message:
        return

    text = message.text or message.caption or ""

    text = text.lower()

    for keyword in KEYWORDS:
        if keyword in text:
            try:
                await message.delete()
                print(f"Deleted message containing: {keyword}")
            except Exception as e:
                print(f"Could not delete message: {e}")

            break


app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(
        filters.UpdateType.CHANNEL_POST,
        check_message
    )
)

print("Bot is running...")

app.run_polling()
