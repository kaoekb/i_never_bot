# config.py
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('Token_tg')
Token_MDB = os.getenv('db')
MONGO_URI = f'mongodb+srv://{Token_MDB}@cluster0.w6k4v.mongodb.net/?retryWrites=true&w=majority'
ADMIN_ID = int(os.getenv('Your_user_ID'))
