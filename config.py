# config.py
import os
import urllib
from dotenv import load_dotenv
# from urllib.parse import quote_plus
import logging

load_dotenv()
BOT_TOKEN = os.getenv('Token_tg')
# DB_USER = os.getenv('DB_USER')
# DB_PASS = os.getenv('DB_PASS')
# db = os.getenv("Token_MDB")

MONGO_URI = 'mongodb+srv://Anton:12345@cluster0.w6k4v.mongodb.net/?retryWrites=true&w=majority'
ADMIN_ID = int(os.getenv('Your_user_ID'))

logging.info(f"[DEBUG] MONGO_URI: {MONGO_URI}")
