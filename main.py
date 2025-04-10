import telebot
import logging
import os
from config import BOT_TOKEN
from bot.handlers import register_handlers
from bot.admin import register_admin_handlers
import bot.database as database

# Убираем старые обработчики и настраиваем логирование
logging.getLogger().handlers.clear()

# Папка для логов
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройки логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{log_dir}/bot.log", mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logging.info("🚀 Бот запускается...")

def start_bot():
    try:
        # Создаем бота
        bot = telebot.TeleBot(BOT_TOKEN)

        # Подключаемся к MongoDB с передачей бота
        database.client = database.connect_to_mongo(bot)
        database.db = database.client["i_never_bot"]
        database.users_collection = database.db["Users"]
        database.ads_collection = database.db["Ads"]
        database.stats_collection = database.db["Stats"]

        # Логируем статистику по коллекциям
        database.log_collections_summary()

        # Регистрируем обработчики
        register_admin_handlers(bot)
        register_handlers(bot)

        # Проверка загрузки обработчиков
        logging.info("📌 Зарегистрированы обработчики:")
        for handler in bot.message_handlers:
            logging.info(f"✔ {handler['filters']}")
        for handler in bot.callback_query_handlers:
            logging.info(f"✔ {handler['filters']}")

        logging.info("🚀 Бот запущен!")
        bot.polling(none_stop=True)

    except Exception as e:
        logging.error(f"❌ Произошла ошибка при запуске бота: {e}")

if __name__ == "__main__":
    start_bot()
