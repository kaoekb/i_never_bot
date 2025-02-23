from telebot import types
import random
from data.question import question
from bot.database import users_collection, ads_collection
import logging

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        users_collection.update_one(
            {"_id": message.from_user.id}, 
            {"$set": {"username": message.from_user.username}}, 
            upsert=True
        )
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Я никогда не...'))
        markup.add(types.KeyboardButton('Правила'), types.KeyboardButton('Проекты'))
        bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, выбери действие.', reply_markup=markup)
    
    @bot.message_handler(content_types=['text'])
    def bot_message(message):
        try:
            text = message.text.lower()
            if text in ['вопрос', 'я никогда не...']:
                bot.send_message(message.chat.id, random.choice(question))
            elif text == 'правила':
                bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, «Я никогда не» это идеальный способ познакомиться поближе с новыми приятелями и узнать много нового о старых друзьях. \n\nИгрокам предстоит по очереди зачитывать фразы которые будут начинаться с «Я никогда не...». В том случае, если для кого-то из игроков эта фраза не является правдой, (то есть он совершал указанное действие), он должен выпить.')
            elif text == 'проекты':
                projects = list(ads_collection.find())
                response = "Другие проекты:\n" + "\n".join([f"- {p['link']}: {p['description']}" for p in projects]) if projects else "Проектов пока нет."
                bot.send_message(message.chat.id, response)
            else:
                bot.send_message(message.chat.id, "Команда не распознана.")
        except Exception as e:
            logging.error(f"Ошибка при обработке сообщения: {e}")
            bot.send_message(message.chat.id, "Произошла ошибка, попробуйте позже.")