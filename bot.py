import telebot
import os
import requests
import pandas as pd
import time

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

CHAT_ID = "8178103030"

symbol = "BTCUSDT"
interval = "15m"

def get_klines():
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=210"
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df = df.iloc[:, :6]
    df.columns = ["time","open","high","low","close","volume"]
    df["close"] = df["close"].astype(float)
    return df

def check_signal():
    df = get_klines()
    df["EMA200"] = df["close"].ewm(span=200).mean()

    last_close = df["close"].iloc[-1]
    last_ema = df["EMA200"].iloc[-1]

    if last_close > last_ema:
        return "📈 BUY SIGNAL (Above EMA 200)"
    elif last_close < last_ema:
        return "📉 SELL SIGNAL (Below EMA 200)"
    else:
        return None

while True:
    signal = check_signal()
    if signal:
        bot.send_message(CHAT_ID, f"BTCUSDT 15m Signal:\n{signal}")
    time.sleep(900)
