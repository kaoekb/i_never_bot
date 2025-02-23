# config.py
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('Token_tg')
MONGO_URI = os.getenv('Token_MDB')
ADMIN_ID = int(os.getenv('Your_user_ID'))
