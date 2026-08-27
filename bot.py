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
    print("UPDATE RECEIVED")

    message = update.channel_post

    if not message:
        print("No channel post found")
        return

    print(f"Message ID: {message.message_id}")
    print(f"Text: {message.text}")
    print(f"Caption: {message.caption}")
    print(f"Has image: {bool(message.photo)}")

    # Delete every image, whether it has a caption or not
    if message.photo:
        try:
            await message.delete()
            print("IMAGE DELETED")
        except Exception as e:
            print(f"COULD NOT DELETE IMAGE: {e}")

        return

    # Check text/captions for keywords
    text = message.text or message.caption or ""
    text = text.lower()

    print(f"Checking text: {text}")

    for keyword in KEYWORDS:
        if keyword in text:
            try:
                await message.delete()
                print(f"DELETED MESSAGE - keyword: {keyword}")
            except Exception as e:
                print(f"COULD NOT DELETE MESSAGE: {e}")

            break


app = Application.builder().token(BOT_TOKEN).build()

# Receive channel posts
app.add_handler(
    MessageHandler(
        filters.UpdateType.CHANNEL_POST,
        check_message
    )
)

print("Bot is running...")

app.run_polling()
