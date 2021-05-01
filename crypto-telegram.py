import os
from dotenv import load_dotenv
import requests
import time
import math

# Load environment (.env) settings.
load_dotenv()
EXCHANGE_RATES_API = os.getenv("EXCHANGE_RATES_API")
TELEGRAM_BOT_API = os.getenv("TELEGRAM_BOT_API")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Threshold settings.
threshold = {
    "bitcoin": {"MAX": 0.00, "MIN": 0.00},
    "ethereum": {"MAX": 0.00, "MIN": 0.00},
    "algorand": {"MAX": 0.00, "MIN": 0.00},
    "dogecoin": {"MAX": 0.00, "MIN": 0.00},
    "solana": {"MAX": 0.00, "MIN": 0.00},
    "dash": {"MAX": 0.00, "MIN": 0.00},
}
# History List
history = {
    "counter": 0,
    "coins": {
        "bitcoin": [],
        "ethereum": [],
        "algorand": [],
        "dogecoin": [],
        "solana": [],
        "dash": [],
    },
}
# Loop interval
time_interval = 60 * 20


def sendMessage(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_API}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&parse_mode=html&text={message}"
    requests.get(url)


def getValue(coin, fiat):
    url = f"{EXCHANGE_RATES_API}ids={coin}&vs_currencies={fiat}"
    response = requests.get(url)
    response_json = response.json()
    price = float(response_json[coin][fiat])
    return price


def updateThreshold(coin, type, value):
    if coin == "bitcoin":
        if type == "MAX":
            threshold[coin][type] = value + 1000.00
        elif type == "MIN":
            threshold[coin][type] = value - 1000.00
    elif coin == "ethereum":
        if type == "MAX":
            threshold[coin][type] = value + 500.00
        elif type == "MIN":
            threshold[coin][type] = value - 500.00
    elif coin == "algorand":
        if type == "MAX":
            threshold[coin][type] = value + 0.05
        elif type == "MIN":
            threshold[coin][type] = value - 0.05
    elif coin == "dogecoin":
        if type == "MAX":
            threshold[coin][type] = value + 0.10
        elif type == "MIN":
            threshold[coin][type] = value - 0.10
    elif coin == "solana":
        if type == "MAX":
            threshold[coin][type] = value + 5
        elif type == "MIN":
            threshold[coin][type] = value - 5
    elif coin == "dash":
        if type == "MAX":
            threshold[coin][type] = value + 25
        elif type == "MIN":
            threshold[coin][type] = value - 25


def calibrateThreshold(coin, fiat):
    price = getValue(coin, fiat)
    price = round(price, 2)
    updateThreshold(coin, "MAX", price)
    updateThreshold(coin, "MIN", price)


def checkCoin(coin, fiat):
    price = getValue(coin, fiat)
    threshold_max = threshold[coin]["MAX"]
    threshold_min = threshold[coin]["MIN"]
    history["coins"][coin].append(price)

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


def showHistory():
    sendMessage(
        f'🚨 <i>ALERT HISTORY GRAPH IN LAST 3 HOURS</i> 🚨\n<b>BITCOIN</b> <code>{history["coins"]["bitcoin"]}</code>\n<b>ETHEREUM</b> <code>{history["coins"]["ethereum"]}</code>\n<b>ALGORAND</b> <code>{history["coins"]["algorand"]}</code>\n<b>DOGECOIN</b> <code>{history["coins"]["dogecoin"]}</code>\n<b>SOLANA</b> <code>{history["coins"]["solana"]}</code>\n<b>DASH</b> <code>{history["coins"]["dash"]}</code>'
    )

    history["counter"] == 0
    for x in history["coins"]:
        history["coins"][x].clear()


sendMessage(f"<b>Crypto-Telegram</b> \n<code>[by arshetamine with love.]</code>")


calibrateThreshold("bitcoin", "eur")
calibrateThreshold("ethereum", "eur")
calibrateThreshold("algorand", "eur")
calibrateThreshold("dogecoin", "eur")
calibrateThreshold("solana", "eur")
calibrateThreshold("dash", "eur")

# -----------------------------------------------------------------
# Main Loop


def main():
    while True:
        print("Getting DATA...")
        history["counter"] += 1

        checkCoin("bitcoin", "eur")
        checkCoin("ethereum", "eur")
        checkCoin("algorand", "eur")
        checkCoin("dogecoin", "eur")
        checkCoin("solana", "eur")
        checkCoin("dash", "eur")

        if history["counter"] == 15:
            showHistory()

        time.sleep(time_interval)


if __name__ == "__main__":
    main()
