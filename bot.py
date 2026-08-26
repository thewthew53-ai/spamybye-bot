import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]

KEYWORDS = [
    "dm",
    "message me",
    "whatsapp.com",
    "boom",
]


async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post

    if not message:
        return

    # Delete every image, whether it has a caption or not
    if message.photo:
        try:
            await message.delete()
            print("Deleted image")
        except Exception as e:
            print(f"Could not delete image: {e}")

        return

    # Check text and captions for keywords
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

# Receive channel posts, including text, images, videos, etc.
app.add_handler(
    MessageHandler(
        filters.UpdateType.CHANNEL_POST,
        check_message
    )
)

print("Bot is running...")

app.run_polling()
