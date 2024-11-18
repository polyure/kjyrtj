import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

KJYR_DATE = datetime(2024, 11, 16, 17, 0, 0).date()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Olen KJYR-tj-botti.")

async def count_days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tj = KJYR_DATE - datetime.now().date()
    if tj.days == 0:
        text = "KJYR-TJ: 0, KJYR is today!"
    elif tj.days == -1:
        text = "KJYR is underway, stop asking and enjoy the cruise!"
    elif tj.days < -1:
        text = "Thank you everyone! See you again at next year's KJYR."
    else:
        tj = str(tj.days)
        text = "KJYR-TJ: " + tj
    await update.effective_message.reply_text(text)
    
    
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    
    application.add_handler(start_handler)
    application.add_handler(CommandHandler("kjyrtj", count_days))
    application.add_handler(CommandHandler("tj", count_days))
    application.add_handler(CommandHandler("tjkjyr", count_days))
    application.add_handler(CommandHandler("tillkjyr", count_days))
    application.add_handler(CommandHandler("countdayskjyr", count_days))
    application.add_handler(CommandHandler("paiviakunneskjyr", count_days))
    application.add_handler(CommandHandler("kjyriimme", count_days))
    application.add_handler(CommandHandler("kjyrcountdown", count_days))
    application.add_handler(CommandHandler("KauankoJaljellaYhteisRisteilyyn", count_days))
    
    application.run_polling()
