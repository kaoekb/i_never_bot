# admin.py
from telebot import types
from bot.database import users_collection, projects_collection, ads_collection
from config import ADMIN_ID
import logging

def register_admin_handlers(bot):
    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        if message.from_user.id == ADMIN_ID:
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Статус", callback_data="status"))
            markup.add(types.InlineKeyboardButton("Удалить проект", callback_data="remove_project"))
            markup.add(types.InlineKeyboardButton("Удалить рекламу", callback_data="remove_ad"))
            bot.send_message(message.chat.id, "Админ-панель", reply_markup=markup)
    
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        if call.data == "status":
            user_count = users_collection.count_documents({})
            bot.send_message(call.message.chat.id, f"Пользователей: {user_count}")
        elif call.data == "remove_project":
            bot.send_message(call.message.chat.id, "Введите ссылку проекта для удаления:")
            bot.register_next_step_handler(call.message, remove_project)
        elif call.data == "remove_ad":
            bot.send_message(call.message.chat.id, "Введите ссылку рекламы для удаления:")
            bot.register_next_step_handler(call.message, remove_ad)

def remove_project(message):
    projects_collection.delete_one({"link": message.text})
    message.bot.send_message(message.chat.id, "Проект удален.")

def remove_ad(message):
    ads_collection.delete_one({"link": message.text})
    message.bot.send_message(message.chat.id, "Реклама удалена.")
