# handlers.py
from telebot import types
import random
from data.question import question
from bot.database import users_collection, projects_collection, ads_collection, stats_collection
from config import ADMIN_ID
import logging

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        users_collection.update_one({"_id": message.from_user.id}, {"$set": {"username": message.from_user.username}}, upsert=True)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Я никогда не...'))
        markup.add(types.KeyboardButton('Правила'), types.KeyboardButton('Проекты'))
        bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, выбери действие.', reply_markup=markup)
    
    @bot.message_handler(content_types=['text'])
    def bot_message(message):
        if message.text == 'Вопрос':
            bot.send_message(message.chat.id, random.choice(question))
        elif message.text == 'Правила':
            bot.send_message(message.chat.id, 'Привет {0.first_name}, «Я никогда не» это идеальный способ познакомиться поближе с новыми приятелями и узнать много нового о старых друзьях. \n\nИгрокам предстоит по очереди зачитывать фразы которые будут начинаться с «Я никогда не...». В том случае, если для кого-то из игроков эта фраза не является правдой, (то есть он совершал указанное действие), он должен выпить.')
        elif message.text == 'Проекты':
            projects = list(projects_collection.find())
            response = "Список проектов:\n" + "\n".join([f"{p['description']}: {p['link']}" for p in projects]) if projects else "Проектов пока нет."
            bot.send_message(message.chat.id, response)
    
    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        if message.from_user.id == ADMIN_ID:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Статус", callback_data="status"))
            bot.send_message(message.chat.id, "Админ-панель", reply_markup=markup)
    
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        if call.data == "status":
            bot.send_message(call.message.chat.id, f"Пользователей: {users_collection.count_documents({})}")
