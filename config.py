import os
from dotenv import load_dotenv

load_dotenv()

STEAM_LOGIN = os.getenv('STEAM_LOGIN')
STEAM_PASSWORD = os.getenv('STEAM_PASSWORD')
