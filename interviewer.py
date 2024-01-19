import asyncio
import telegram
import openai
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler, CallbackContext, ConversationHandler

CONVERSATION, SETJOB, SETSKILL = range(3)
openai.api_key = '***'
TGTOKEN = '6665952817:AAF_dnASVlIvQYULrRBRvSHO202ugysZ5hk'

user_skills = {}
user_job = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update, context):
        await update.message.reply_text("Hello there!\n\nUse /help to see how to use bot")
        return CONVERSATION

async def set(update, context):
    await update.message.reply_text("What job do you want to interview")
    return SETJOB
    
async def setjob(update,context):
    user_id = update.effective_user.id
    user_job[user_id] = update.message.text
    await update.message.reply_text(f'Your requested job is: \'{user_job[user_id]}\'\nNow enter your skills')
    return SETSKILL
async def setskill(update,context):
    user_id = update.effective_user.id
    user_skills[user_id] = update.message.text
    await update.message.reply_text(f'Your skills: \n\'{user_skills[user_id]}\'')


if __name__ == '__main__':
    application = ApplicationBuilder().token(TGTOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CONVERSATION: [
                CommandHandler('setting', set),
            ],
            SETSKILL: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), setskill)
            ],
            SETJOB: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), setjob)
            ],
        },
        fallbacks=[],
        allow_reentry=True
    )


    application.add_handler(conv_handler)

    application.run_polling()
