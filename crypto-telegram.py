import os
from dotenv import load_dotenv
import requests
import time
import math

# Load environment (.env) settings.
load_dotenv()
EXCHANGE_RATES_URL = os.getenv('EXCHANGE_RATES_URL')
TELEGRAM_BOT_API = os.getenv('TELEGRAM_BOT_API')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Threshold settings.
threshold = {
    'BTC': {'MAX': 0.00, 'MIN': 0.00},
    'ETH': {'MAX': 0.00, 'MIN': 0.00},
    'ALGO': {'MAX': 0.00, 'MIN': 0.00},
}

history = {'BTC': [], 'ETH': [], 'ALGO': []}

delay = 60 * 5


def sendMessage(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_API}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&parse_mode=html&text={message}'
    requests.get(url)


def getValue(coin, fiat):
    url = f'{EXCHANGE_RATES_URL}{coin}-{fiat}/spot'
    response = requests.get(url)
    response_json = response.json()
    price = float(response_json['data']['amount'])
    return price

# -----------------------------------------------------------------


def updateThreshold(coin, type, value):
    if coin == 'BTC':
        if type == 'MAX':
            threshold[coin][type] = value + 500.00
        elif type == 'MIN':
            threshold[coin][type] = value - 500.00
    elif coin == 'ETH':
        if type == 'MAX':
            threshold[coin][type] = value + 100.00
        elif type == 'MIN':
            threshold[coin][type] = value - 100.00
    elif coin == 'ALGO':
        if type == 'MAX':
            threshold[coin][type] = value + 0.05
        elif type == 'MIN':
            threshold[coin][type] = value - 0.05


def calibrateThreshold(coin, fiat):
    price = getValue(coin, fiat)
    price = round(price, 2)
    updateThreshold(coin, "MAX", price)
    updateThreshold(coin, "MIN", price)
    max = round(threshold[coin]['MAX'], 2)
    min = round(threshold[coin]['MIN'], 2)
    sendMessage(
        f'🔧 <b>{coin}</b> CALIBRATING: <code>{price}</code> <i>{fiat}</i>\n<i>calibrated threshold - MAX: {max} - MIN: {min} {fiat}</i>')


def checkCoin(coin, fiat):
    price = getValue(coin, fiat)
    threshold_max = threshold[coin]["MAX"]
    threshold_min = threshold[coin]["MIN"]

    history[coin].append(price)

    if price >= threshold_max:
        calibrateThreshold(coin, fiat)
        sendMessage(
            f'⚠️ <b>{coin}</b> Rise Signal: <code>{price}</code> <i>{fiat}</i> 📈\n<i>current threshold - {round(threshold_max, 2)} {fiat}</i>\n[AI] <i>calibrated threshold - {round(threshold[coin]["MAX"], 2)} {fiat}</i>')

    elif price <= threshold_min:
        calibrateThreshold(coin, fiat)
        sendMessage(
            f'⚠️ <b>{coin}</b> Down Signal: <code>{price}</code> <i>{fiat}</i> 📉\n<i>current threshold - {round(threshold_min, 2)} {fiat}</i>\n[AI] <i>calibrated threshold - {round(threshold[coin]["MIN"], 2)} {fiat}</i>')


def checkAll():
    checkCoin('BTC', 'EUR')
    checkCoin('ETH', 'EUR')
    checkCoin('ALGO', 'EUR')
    print("Checked all.")
    time.sleep(delay)


def startChecker():
    while True:
        checkAll()


sendMessage(
    f'<b>Crypto-Telegram</b> \n<code>[by arshetamine with love.]</code>')

time.sleep(5)
calibrateThreshold('BTC', 'EUR')
calibrateThreshold('ETH', 'EUR')
calibrateThreshold('ALGO', 'EUR')

startChecker()
