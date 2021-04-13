import os
from dotenv import load_dotenv
import requests
import time

# Load environment (.env) settings.
load_dotenv()
EXCHANGE_API = os.getenv('EXCHANGE_API')
TELEGRAM_BOT_API = os.getenv('TELEGRAM_BOT_API')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def sendMessage(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&parse_mode=html&text={message}"
    requests.get(url)


sendMessage("Hello World!")
