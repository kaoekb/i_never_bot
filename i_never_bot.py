import telebot
import random
from telebot import types
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from question import question
bot = telebot.TeleBot(os.getenv('Token_tg'))


class DataBase:
    def __init__(self):
        cluster = MongoClient(os.getenv('Token_MDB'))
        self.db = cluster["I_never"]
        self.users = self.db["Users"]

    def add_user(self, user_id, username):
        user_data = {
            "_id": user_id,
            "username": username,
            "last_interaction": datetime.now()
        }
        self.users.update_one({"_id": user_id}, {"$set": user_data}, upsert=True)

    def update_last_interaction(self, user_id):
        self.users.update_one({"_id": user_id}, {"$set": {"last_interaction": datetime.now()}})


db = DataBase()

@bot.message_handler(commands=['start', 'Я никогда не...'])
def send_welcome(message):
    db.add_user(message.from_user.id, message.from_user.username)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Я никогда не...')
    markup.add(item)
    bot.send_message(message.chat.id, '  Привет {0.first_name}, «Я никогда не» это идеальный способ познакомиться поближе с новыми приятелями и узнать много нового о старых друзьях. \n\nИгрокам предстоит по очереди зачитывать фразы которые будут начинаться с «Я никогда не...». В том случае, если для кого-то из игроков эта фраза не является правдой, (то есть он совершал указанное действие), он должен выпить.'.format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Я никогда не...':
            answer_message = random.choice(question)
            bot.send_message(message.chat.id, answer_message)
            db.update_last_interaction(message.from_user.id)


bot.polling()
