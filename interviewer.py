import asyncio
import telegram
import openai
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler, CallbackContext, ConversationHandler
  
openai.api_key = '***'
TGTOKEN = '***'

class User:
    job = ''
    skills = ''
    started = False

buser = User

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update,context1):
    user_id = update.effective_user.id
    buser[user_id].started = True
    await update.message.reply_text("Hello there\n\nUse /help to see how to use bot")

async def set(update, context):
    


if __name__ == '__main__':
    
    application = ApplicationBuilder().token(TGTOKEN).build()
    conv_handler = ConversationHandler(
        entry_points= [CommandHandler("start",start)],
        states= [
            CommandHandler("setting",set),

        ]
    )

    application.run_polling()

