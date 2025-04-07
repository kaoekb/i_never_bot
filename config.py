# config.py
import os
import urllib
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('Token_tg')
# Token_MDB = os.getenv('db')
# Token_MDB = urllib.parse.quote_plus(Token_MDB)  # Кодируем символы в пароле

# MONGO_URI = f'mongodb+srv://{Token_MDB}@cluster0.w6k4v.mongodb.net/?retryWrites=true&w=majority'

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

MONGO_URI = f'mongodb+srv://{DB_USER}:{DB_PASS}@cluster0.w6k4v.mongodb.net/?retryWrites=true&w=majority'

ADMIN_ID = int(os.getenv('Your_user_ID'))
