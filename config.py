# config.py
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()
BOT_TOKEN = int(os.getenv('Token_tg'))
Token_MDB = os.getenv('db')
# MONGO_URI = f'mongodb+srv://{db}@cluster0.w6k4v.mongodb.net/?retryWrites=true&w=majority'

# Экранируем токен
encoded_token = urllib.parse.quote_plus(Token_MDB)

# Используем закодированный токен в строке подключения
MONGO_URI = f'mongodb+srv://{encoded_token}@cluster0.w6k4v.mongodb.net/?retryWrites=true&w=majority'

ADMIN_ID = int(os.getenv('Your_user_ID'))
