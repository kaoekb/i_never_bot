from telebot import types
import random
from data.question import question
import logging
import bot.database as db  # Импортируем модуль database целиком

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        # Обновляем пользователя в базе
        db.users_collection.update_one(
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
                bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, «Я никогда не» — это идеальный способ познакомиться поближе с новыми приятелями и узнать много нового о старых друзьях. \n\nИгрокам предстоит по очереди зачитывать фразы, начинающиеся с «Я никогда не...». Если для кого-то эта фраза не является правдой, он должен выпить.')
            elif text == 'проекты':
                projects = list(db.ads_collection.find())
                if projects:
                    response = "Другие проекты:\n" + "\n".join([f"- {p['link']}: {p['description']}" for p in projects])
                else:
                    response = "Проектов пока нет."
                bot.send_message(message.chat.id, response)
            else:
                bot.send_message(message.chat.id, "Команда не распознана.")
        except Exception as e:
            logging.error(f"Ошибка при обработке сообщения: {e}")
            bot.send_message(message.chat.id, "Произошла ошибка, попробуйте позже.")
