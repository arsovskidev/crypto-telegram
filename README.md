# Crypto-Telegram

![](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Farshetamine%2FCrypto-Telegram&count_bg=%23A4B6F7&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)

#### Telegram BOT for alerting crypto currency price changes &amp; historical data.

###### Create virtual environment and install requirements.

```
$ sudo apt-get install python3-venv
$ python3 -m venv crypto-telegram
$ source crypto-telegram/bin/activate
$ touch .env
$ pip3 install -r requirements.txt
$ python3 crypto-telegram.py
```

###### In the .env file enter the following settings.

```
$ nano .env

EXCHANGE_API = [YOUR EXCHANGE RATES API]
TELEGRAM_BOT_API = [YOUR BOT API]
TELEGRAM_CHAT_ID = [YOUR CHAT ID]

```
