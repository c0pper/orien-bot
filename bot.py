import os
import json
import random
import logging
import rx
from telegram import Update
# noinspection PyUnresolvedReferences
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

HEROKU_URL = "https://orien-bot.herokuapp.com/"
PORT = int(os.environ.get('PORT', '8433'))
TELE_TOKEN = os.environ.get('bot-token')

# Assets

picfile = 'pics.txt'
quotefile = 'quotes.txt'

with open(picfile) as p, open(quotefile) as q:
    plines = p.readlines()
    qlines = q.readlines()


# Define Command Handlers
def start(update: Update, context: CallbackContext):
    """Handler for /start command"""
    update.message.reply_text('we')


def userText(update: Update, context: CallbackContext):
    """Function to reply to user text"""
    quote = random.choice(qlines)
    update.message.reply_text(quote)


# def send_audio(update: Update, context: CallbackContext) -> None:
#     audio = random.choice(alines)
#     update.message.reply_voice(audio)


def send_rand_photo(update: Update, context: CallbackContext) -> None:
    photo = random.choice(plines)
    update.message.reply_photo(photo, random.choice(qlines))


def main():
    """starting bot"""
    updater = Updater(TELE_TOKEN, use_context=True)

    # getting the dispatchers to register handlers
    dp = updater.dispatcher

    # registering commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("lattosio", send_rand_photo))
    # registering Message Handler to reply to user messages
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(rx.trigger_regex) & ~Filters.command, userText))

    # starting the bot
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TELE_TOKEN,
                          webhook_url=HEROKU_URL + TELE_TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
