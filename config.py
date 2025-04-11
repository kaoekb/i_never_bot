# config.py
import os
import urllib
from dotenv import load_dotenv
import logging

load_dotenv()
BOT_TOKEN = os.getenv('Token_tg')
db = os.getenv("Token_MDB")

MONGO_URI = f'mongodb+srv://{db}5@cluster0.w6k4v.mongodb.net/?retryWrites=true&w=majority'
ADMIN_ID = int(os.getenv('Your_user_ID'))
