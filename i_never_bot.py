import telebot
import random
from telebot import types
from pymongo import MongoClient, errors
from datetime import datetime
import os
from dotenv import load_dotenv, find_dotenv
import logging
from question import question
import time

# Загрузка переменных окружения
load_dotenv(find_dotenv())

# Настройка логирования
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file_path = os.path.join(log_dir, "bot.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

def connect_to_mongo():
    while True:
        try:
            mongo_uri = os.getenv('Token_MDB')
            cluster = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            cluster.server_info()  # Проверка соединения
            logging.info("Подключение к MongoDB успешно!")
            return cluster
        except errors.ServerSelectionTimeoutError:
            logging.error("Ошибка подключения к MongoDB. Повторная попытка через 5 секунд...")
            time.sleep(5)

# Подключение к MongoDB с повторными попытками
cluster = connect_to_mongo()
db = cluster["i_never"]
users_collection = db["Users"]
projects_collection = db["Projects"]
ads_collection = db["Ads"]
stats_collection = db["Stats"]

admin_user_id = int(os.getenv('Your_user_ID'))

bot = telebot.TeleBot(os.getenv('Token_tg'))

def update_last_interaction(user_id):
    users_collection.update_one({"_id": user_id}, {"$set": {"last_interaction": datetime.now()}}, upsert=True)

def get_user_count():
    return users_collection.count_documents({})

def increment_question_access():
    stats_collection.update_one({}, {"$inc": {"questions_accessed": 1}}, upsert=True)

def get_question_access_count():
    stat = stats_collection.find_one()
    return stat.get("questions_accessed", 0) if stat else 0

def get_projects():
    return list(projects_collection.find())

def get_ads():
    return list(ads_collection.find())

def send_logs(message):
    if os.path.exists(log_file_path):
        with open(log_file_path, 'rb') as log_file:
            bot.send_document(message.chat.id, log_file)
    else:
        bot.send_message(message.chat.id, "Файл логов не найден.")

def notify_admin(text):
    bot.send_message(admin_user_id, f"🔔 Уведомление: {text}")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    users_collection.update_one({"_id": message.from_user.id}, {"$set": {"username": message.from_user.username, "last_interaction": datetime.now()}}, upsert=True)
    notify_admin(f"Новый пользователь: {message.from_user.username} ({message.from_user.id})")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Вопрос'))
    markup.add(types.KeyboardButton('Правила'), types.KeyboardButton('Проекты'))
    bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, готов начать игру? Выберите действие.', reply_markup=markup)

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == admin_user_id:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Статус", callback_data="status"))
        markup.add(types.InlineKeyboardButton("Логи", callback_data="logs"))
        markup.add(types.InlineKeyboardButton("Удалить проект", callback_data="remove_project"))
        markup.add(types.InlineKeyboardButton("Удалить рекламу", callback_data="remove_ad"))
        bot.send_message(message.chat.id, "Добро пожаловать в админку!", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "У вас нет прав для доступа к этой команде.")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.data == "status":
            bot.send_message(call.message.chat.id, f"Пользователей: {get_user_count()}\nЗапросов вопросов: {get_question_access_count()}")
        elif call.data == "logs":
            send_logs(call.message)
        elif call.data == "remove_project":
            bot.send_message(call.message.chat.id, "Введите ссылку проекта для удаления:")
            bot.register_next_step_handler(call.message, remove_project)
        elif call.data == "remove_ad":
            bot.send_message(call.message.chat.id, "Введите ссылку рекламы для удаления:")
            bot.register_next_step_handler(call.message, remove_ad)
    except Exception as e:
        logging.error(f"Ошибка в callback_inline: {e}")
        bot.send_message(call.message.chat.id, "Произошла ошибка.")

def remove_project(message):
    projects_collection.delete_one({"link": message.text})
    bot.send_message(message.chat.id, "Проект удален.")
    notify_admin(f"Удален проект: {message.text}")

def remove_ad(message):
    ads_collection.delete_one({"link": message.text})
    bot.send_message(message.chat.id, "Реклама удалена.")
    notify_admin(f"Удалена реклама: {message.text}")

bot.polling(none_stop=True)
