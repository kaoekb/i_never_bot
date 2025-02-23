import telebot
import logging
import os
from config import BOT_TOKEN
from bot.handlers import register_handlers
from bot.admin import register_admin_handlers

# Убираем старые обработчики (если они есть) и настраиваем логирование
logging.getLogger().handlers.clear()

# Папка для логов
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройки логирования
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{log_dir}/bot.log", mode='a', encoding='utf-8'),
        logging.StreamHandler()  # Вывод логов в консоль
    ]
)

# Логирование старта
logging.info("🚀 Бот запускается...")

def start_bot():
    try:
        # Создаем объект бота
        bot = telebot.TeleBot(BOT_TOKEN)

        # Регистрируем обработчики
        register_admin_handlers(bot)
        register_handlers(bot)

        # Проверяем, загружаются ли обработчики
        logging.info("📌 Зарегистрированы обработчики:")
        for handler in bot.message_handlers:
            logging.info(f"✔ {handler['filters']}")
        for handler in bot.callback_query_handlers:
            logging.info(f"✔ {handler['filters']}")

        # Запуск бота
        logging.info("🚀 Бот запущен!")
        bot.polling(none_stop=True)  # Ожидаем и обрабатываем сообщения

    except Exception as e:
        logging.error(f"Произошла ошибка при запуске бота: {e}")

# Проверяем, что скрипт выполняется напрямую
if __name__ == "__main__":
    start_bot()
