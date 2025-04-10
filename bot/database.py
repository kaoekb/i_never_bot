# bot/database.py
from pymongo import MongoClient, errors
from config import MONGO_URI
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Переменные будут инициализированы позже в main.py
client = None
db = None
users_collection = None
ads_collection = None
stats_collection = None

def connect_to_mongo(bot=None):
    from bot.utils import notify_admin
    while True:
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.server_info()
            logger.info("✅ Успешное подключение к MongoDB")
            return client
        except errors.ServerSelectionTimeoutError:
            logger.error("1❌ Ошибка подключения к MongoDB. Повторная попытка через 5 секунд...")
            time.sleep(5)
        except Exception as e:
            logger.critical("1❌ Критическая ошибка MongoDB: %s", str(e))
            if bot:
                notify_admin(bot, f"1❌ Критическая ошибка подключения к MongoDB:\n{e}")
            time.sleep(5)

def log_collections_summary():
    global users_collection, ads_collection, stats_collection
    try:
        users_count = users_collection.count_documents({})
        ads_count = ads_collection.count_documents({})
        stats_count = stats_collection.count_documents({})
        logger.info(f"📊 Статистика коллекций: Users={users_count}, Ads={ads_count}, Stats={stats_count}")
    except Exception as e:
        logger.error("⚠ Ошибка при получении статистики коллекций: %s", str(e))
