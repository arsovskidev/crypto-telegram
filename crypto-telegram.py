import os
from dotenv import load_dotenv
import requests
import time
import math

# Load environment (.env) settings.
load_dotenv()
EXCHANGE_RATES_URL = os.getenv("EXCHANGE_RATES_URL")
TELEGRAM_BOT_API = os.getenv("TELEGRAM_BOT_API")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Threshold settings.
threshold = {
    "bitcoin": {"MAX": 0.00, "MIN": 0.00},
    "ethereum": {"MAX": 0.00, "MIN": 0.00},
    "algorand": {"MAX": 0.00, "MIN": 0.00},
}
# History List
history = {"counter": 0, "bitcoin": [], "ethereum": [], "algorand": []}
# Loop interval
time_interval = 60 * 10


def sendMessage(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&parse_mode=html&text={message}"
    requests.get(url)


def getValue(coin, fiat):
    url = f"{EXCHANGE_RATES_URL}ids={coin}&vs_currencies={fiat}"
    response = requests.get(url)
    response_json = response.json()
    price = float(response_json[coin][fiat])
    return price


def updateThreshold(coin, type, value):
    if coin == "bitcoin":
        if type == "MAX":
            threshold[coin][type] = value + 500.00
        elif type == "MIN":
            threshold[coin][type] = value - 500.00
    elif coin == "ethereum":
        if type == "MAX":
            threshold[coin][type] = value + 100.00
        elif type == "MIN":
            threshold[coin][type] = value - 100.00
    elif coin == "algorand":
        if type == "MAX":
            threshold[coin][type] = value + 0.05
        elif type == "MIN":
            threshold[coin][type] = value - 0.05


def calibrateThreshold(coin, fiat):
    price = getValue(coin, fiat)
    price = round(price, 2)
    updateThreshold(coin, "MAX", price)
    updateThreshold(coin, "MIN", price)


def checkCoin(coin, fiat):
    price = getValue(coin, fiat)
    threshold_max = threshold[coin]["MAX"]
    threshold_min = threshold[coin]["MIN"]

    history[coin].append(price)

    if price >= threshold_max:
        calibrateThreshold(coin, fiat)
        sendMessage(
            f'​⬆️​ <b>{coin.upper()}</b> Rise Signal: <code>{price}</code> <i>{fiat.upper()}</i> 📈\n<i>current threshold - {round(threshold_max, 2)} {fiat.upper()}</i>\n[AI] <i>calibrated threshold - {round(threshold[coin]["MAX"], 2)} {fiat.upper()}</i>'
        )

    elif price <= threshold_min:
        calibrateThreshold(coin, fiat)
        sendMessage(
            f'⬇️ <b>{coin.upper()}</b> Down Signal: <code>{price}</code> <i>{fiat.upper()}</i> 📉\n<i>current threshold - {round(threshold_min, 2)} {fiat.upper()}</i>\n[AI] <i>calibrated threshold - {round(threshold[coin]["MIN"], 2)} {fiat.upper()}</i>'
        )


sendMessage(f"<b>Crypto-Telegram</b> \n<code>[by arshetamine with love.]</code>")

time.sleep(5)

calibrateThreshold("bitcoin", "eur")
calibrateThreshold("ethereum", "eur")
calibrateThreshold("algorand", "eur")


# -----------------------------------------------------------------
# Main Loop


def main():
    while True:
        print("Getting DATA...")
        checkCoin("bitcoin", "eur")
        checkCoin("ethereum", "eur")
        checkCoin("algorand", "eur")

        time.sleep(time_interval)


if __name__ == "__main__":
    main()
