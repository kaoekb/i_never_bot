# database.py
from pymongo import MongoClient, errors
from config import MONGO_URI
import logging
import time
from bot.utils import notify_admin

# Настройка логгера с указанием времени
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def connect_to_mongo():
    while True:
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.server_info()
            logger.info("✅ Успешное подключение к MongoDB")
            return client
        except errors.ServerSelectionTimeoutError:
            logger.error("❌ Ошибка подключения к MongoDB. Повторная попытка через 5 секунд...")
            time.sleep(5)
        except Exception as e:
            logger.critical(f"❌ Критическая ошибка MongoDB: {e}")
            notify_admin(f"❌ Критическая ошибка подключения к MongoDB: {e}")
            time.sleep(5)

client = connect_to_mongo()
db = client["i_never_bot"]
users_collection = db["Users"]
ads_collection = db["Ads"]
stats_collection = db["Stats"]
