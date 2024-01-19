import asyncio
import telegram
import openai
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler, CallbackContext, ConversationHandler

CONVERSATION, SETJOB, SETSKILL, INTERVIEW = range(4)
openai.api_key = '*****'
TGTOKEN = '*****'

user_chat_history = {}
user_skills = {}
user_job = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update, context):
    await update.message.reply_text("Hello there!\n\nUse /about to see how to use bot")
    return CONVERSATION

async def about(update, context):
    await update.message.reply_text('This bot will simulate interview for a job\n\nfirst use /setting to setup the bot and then use /interview \n\nlist of the commands in /commands\n\nGithub link : https://github.com/mjavadhm/interviewer_bot/')

async def commandsa(update, contex):
    await update.message.reply_text("/start -> restart bot\n\n/interview -> start interview(use /setting first)\n\n/setting -> Choose job for interview")

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
    await update.message.reply_text('Done')
    return CONVERSATION

async def instart(update,context):
    user_id = update.effective_user.id
    if user_id not in user_job or not user_job[user_id]:
        await update.message.reply_text('You need to set the job first using /setting command.')
        return CONVERSATION
    
    await update.message.reply_text(f'This is an interview for \'{user_job[user_id]}\'\n\nUse /end for stop the interview')
    return INTERVIEW

async def end(update,context):
    await update.message.reply_text('Interview ended')
    user_id = update.effective_user.id
    user_chat_history[user_id] = []
    return CONVERSATION

async def reply_to_message(update: Update, context: CallbackContext):
    user_input = update.message.text
    user_id = update.effective_user.id

    if user_id not in user_chat_history:
        user_chat_history[user_id] = []

    user_chat_history[user_id].append({"role": "user", "content": user_input})

    await context.bot.send_chat_action(chat_id=update.message.chat_id , action = telegram.constants.ChatAction.TYPING)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[{"role": "system", "content": f'I want you to act as an interviewer. The person who ask you will be the candidate and you will ask me the interview questions for the position of {user_job[user_id]} and his/her skills are {user_skills[user_id]}(you speak in language that she/he talk to you). I want you to only reply as the interviewer.say hi once and dont say hi in any languages in every questions. Do not write all the conservation at once. I want you to only do the interview with me. Ask me the questions and wait for my answers. Do not write explanations. Ask me the questions one by one like an interviewer does and wait for my answers.' }, *user_chat_history[user_id]],
        n=1,
        stop=None
    )

    await update.message.reply_text(response.choices[0].message['content'])

if __name__ == '__main__':
    application = ApplicationBuilder().token(TGTOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            INTERVIEW: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), reply_to_message),
                CommandHandler('end', end),
            ],
            CONVERSATION: [
                CommandHandler('setting', set),
                CommandHandler('interview',instart),
                CommandHandler('about',about),
                CommandHandler('commands',commandsa),
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
