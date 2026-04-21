import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Load environment variables
load_dotenv()

# Get the bot token from environment variables
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("No TOKEN found in environment variables")

# Set the KJYR date
KJYR_DATE = datetime(2024, 11, 16, 17, 0, 0).date()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define the start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Olen KJYR-tj-botti.")

# Define the count_days command handler
async def count_days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        tj = KJYR_DATE - datetime.now().date()
        if tj.days == 0:
            text = "KJYR-TJ: 0, KJYR is today!"
        elif tj.days == -1:
            text = "KJYR is underway, stop asking and enjoy the cruise!"
        elif tj.days < -1:
            text = "Thank you everyone! See you again at next year's KJYR."
        else:
            text = f"KJYR-TJ: {tj.days}"
        await update.effective_message.reply_text(text)
    except Exception as e:
        logging.error(f"Error in count_days: {e}")
        await update.effective_message.reply_text("An error occurred while processing your request.")

# Main function to start the bot
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Register command handlers
    start_handler = CommandHandler('start', start)
    count_days_handler = CommandHandler(
        ["kjyrtj", "tj", "tjkjyr", "tillkjyr", "countdayskjyr", "paiviakunneskjyr", "kjyriimme"], count_days
    )

    application.add_handler(start_handler)
    application.add_handler(count_days_handler)

    # Start the bot
    application.run_polling()