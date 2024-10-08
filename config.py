import os
from dotenv import load_dotenv

load_dotenv()

STEAM_LOGIN = os.getenv('STEAM_LOGIN')
STEAM_PASSWORD = os.getenv('STEAM_PASSWORD')
API_TOKEN = os.getenv('API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
API_KEY = os.getenv('API_KEY')
