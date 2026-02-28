#config.py
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_KEY = os.getenv("SPREADSHEET_KEY")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")