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
    sendMessage(
        f'🔧 <b>{coin}</b> CALIBRATING: <code>{price}</code> <i>{fiat}</i>\n<i>calibrated threshold - {threshold[coin]} {fiat}</i>')


def checkCoin(coin, fiat):
    price = getValue(coin, fiat)
    threshold_max = threshold[coin]["MAX"]
    threshold_min = threshold[coin]["MIN"]

    history[coin].append(price)

    if price >= threshold_max:
        updateThreshold(coin, "MAX", price)
        sendMessage(
            f'⚠️ <b>{coin}</b> Rise Signal: <code>{price}</code> <i>{fiat}</i> 📈\n<i>current threshold - {threshold_max} {fiat}</i>\n[AI] <i>calibrated threshold - {threshold[coin]["MAX"]} {fiat}</i>')

    elif price <= threshold_min:
        updateThreshold(coin, "MIN", price)
        sendMessage(
            f'⚠️ <b>{coin}</b> Down Signal: <code>{price}</code> <i>{fiat}</i> 📉\n<i>current threshold - {threshold_min} {fiat}</i>\n[AI] <i>calibrated threshold - {threshold[coin]["MIN"]} {fiat}</i>')


# sendMessage(
#     f'<b>Crypto-Telegram</b> <code>[Machine Learning]</code>\n<i>Project created by arshetamine with love.</i>')
# time.sleep(5)
calibrateThreshold('BTC', 'EUR')
calibrateThreshold('ETH', 'EUR')
calibrateThreshold('ALGO', 'EUR')

# checkCoin('BTC', 'EUR')
# checkCoin('ETH', 'EUR')
# checkCoin('ALGO', 'EUR')
print(threshold)
