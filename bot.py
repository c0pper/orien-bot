import telebot
import random
from flask import Flask, request
import os

bot_token = os.environ.get('bot_token')
bot = telebot.TeleBot(token=bot_token)
server = Flask(__name__)

picfile = 'pics.txt'
quotefile = 'quotes.txt'

with open(picfile) as p, open(quotefile) as q:
    plines = p.readlines()
    qlines = q.readlines()


@bot.message_handler(commands=['lattosio'])
def send_rand_photo(message):
    photo = random.choice(plines)
    bot.send_photo(message.chat.id, photo, random.choice(qlines))


@bot.message_handler(commands=['cheesecake'])
def send_rand_quote(message):
    quote = random.choice(qlines)
    bot.send_message(message.chat.id, quote)


@bot.message_handler(func=lambda msg: msg.text is not None and 'orien' in msg.text)
def at_answer(message):
    quote = random.choice(qlines)
    bot.reply_to(message, quote)


@server.route('/' + bot_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://orien-bot.herokuapp.com/' + bot_token)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
