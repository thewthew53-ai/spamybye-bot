import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def filter_channel_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post and update.channel_post.text:
        text_lower = update.channel_post.text.lower()
        if "dm" in text_lower:
            try:
                await context.bot.delete_message(
                    chat_id=update.channel_post.chat.id,
                    message_id=update.channel_post.message_id
                )
                print(f"Deleted spam: '{update.channel_post.text}'")
            except Exception as e:
                print(f"Deletion failed: {e}")

def main():
    TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN!")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL & filters.TEXT, filter_channel_posts))

    print("Bot starting up...")
    application.run_polling()

if __name__ == '__main__':
    main()
