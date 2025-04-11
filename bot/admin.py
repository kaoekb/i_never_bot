from telebot import types
import logging
import os
import bot.database as db
from config import ADMIN_ID
from bot.utils import notify_admin

logging.basicConfig(level=logging.INFO)

admin_bot = None

def register_admin_handlers(bot):
    global admin_bot
    admin_bot = bot

    @bot.message_handler(commands=['admin'])
    def admin_panel(message):
        logging.info(f"Команда /admin от пользователя с ID: {message.from_user.id}")
        try:
            if message.from_user.id != ADMIN_ID:
                logging.warning(f"Попытка доступа к админ-панели от пользователя с ID: {message.from_user.id}")
                bot.send_message(message.chat.id, "❌ У вас нет прав доступа!")
                return

            # Формируем меню админ-панели
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("Статус", callback_data="status"))
            markup.add(types.InlineKeyboardButton("Удалить рекламу", callback_data="remove_ad"))
            markup.add(types.InlineKeyboardButton("Логи", callback_data="logs"))
            markup.add(types.InlineKeyboardButton("Добавить рекламу", callback_data="add_ad"))
            bot.send_message(message.chat.id, "🔹 Админ-панель", reply_markup=markup)

        except Exception as e:
            logging.error(f"Ошибка в админ-панели: {e}")
            bot.send_message(message.chat.id, "❌ Ошибка. Попробуйте позже.")

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        try:
            logging.info(f"Получен callback: {call.data} от пользователя с ID: {call.from_user.id}")

            if call.data == "status":
                user_count = db.users_collection.count_documents({})
                admin_bot.send_message(call.message.chat.id, f"👥 Пользователей: {user_count}")

            elif call.data == "remove_ad":
                admin_bot.send_message(call.message.chat.id, "✏ Введите ссылку рекламы для удаления:")
                bot.register_next_step_handler(call.message, remove_ad)

            elif call.data == "logs":
                send_logs(call.message)

            elif call.data == "add_ad":
                admin_bot.send_message(call.message.chat.id, "✏ Введите ссылку и описание рекламы (через |):")
                bot.register_next_step_handler(call.message, add_ad)

        except Exception as e:
            logging.error(f"Ошибка в обработке callback: {e}")
            admin_bot.send_message(call.message.chat.id, "❌ Ошибка. Попробуйте позже.")

def remove_ad(message):
    try:
        logging.info(f"Удаление рекламы с ссылкой: {message.text}")
        result = db.ads_collection.delete_one({"link": message.text})
        if result.deleted_count > 0:
            admin_bot.send_message(message.chat.id, "✅ Реклама удалена.")
        else:
            admin_bot.send_message(message.chat.id, "❌ Реклама не найдена.")
    except Exception as e:
        logging.error(f"Ошибка удаления рекламы: {e}")
        admin_bot.send_message(message.chat.id, "❌ Ошибка при удалении рекламы.")

def add_ad(message):
    try:
        logging.info(f"Добавление рекламы с текстом: {message.text}")
        parts = message.text.split("|")
        if len(parts) != 2:
            admin_bot.send_message(message.chat.id, "❌ Неверный формат. Используйте: ссылка | описание")
            return
        db.ads_collection.insert_one({
            "link": parts[0].strip(),
            "description": parts[1].strip()
        })
        admin_bot.send_message(message.chat.id, "✅ Реклама добавлена.")
    except Exception as e:
        logging.error(f"Ошибка добавления рекламы: {e}")
        admin_bot.send_message(message.chat.id, "❌ Ошибка при добавлении рекламы.")

def send_logs(message):
    import os
    try:
        log_file_path = "logs/bot.log"
        if not os.path.exists(log_file_path):
            admin_bot.send_message(message.chat.id, "❌ Лог-файл не найден.")
            return
        if not os.access(log_file_path, os.R_OK):
            admin_bot.send_message(message.chat.id, "❌ Нет прав для чтения лог-файла.")
            return
        with open(log_file_path, "rb") as log_file:
            try:
                admin_bot.send_document(message.chat.id, log_file)
                logging.info("Лог-файл успешно отправлен.")
            except Exception as send_error:
                logging.error(f"Ошибка при отправке лог-файла: {send_error}")
                admin_bot.send_message(message.chat.id, "❌ Ошибка при отправке логов.")
    except Exception as e:
        logging.error(f"Ошибка при подготовке логов: {e}")
        admin_bot.send_message(message.chat.id, "❌ Ошибка при отправке логов.")
