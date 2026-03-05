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

last_signal = None

def get_data():
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=250"
        data = requests.get(url).json()
        df = pd.DataFrame(data)
        df = df.iloc[:, :6]
        df.columns = ["time","open","high","low","close","volume"]
        df = df.astype(float)
        return df
    except:
        return None

def check_signal():
    global last_signal
    df = get_data()

    if df is None:
        return None

    df["EMA200"] = df["close"].ewm(span=200).mean()

    last_close = df["close"].iloc[-1]
    last_high = df["high"].iloc[-1]
    last_low = df["low"].iloc[-1]
    ema = df["EMA200"].iloc[-1]

    highest_high = df["high"].iloc[-21:-1].max()
    lowest_low = df["low"].iloc[-21:-1].min()

    if last_close > ema and last_high > highest_high:
        if last_signal != "BUY":
            last_signal = "BUY"
            return "📈 BUY SIGNAL"

    if last_close < ema and last_low < lowest_low:
        if last_signal != "SELL":
            last_signal = "SELL"
            return "📉 SELL SIGNAL"

    return None

# Bot started message
bot.send_message(CHAT_ID, "🤖 Bot is Active and Monitoring Market...")

while True:
    try:
        signal = check_signal()
        if signal:
            bot.send_message(CHAT_ID, f"BTCUSDT 15m\n{signal}")
        time.sleep(60)
    except:
        time.sleep(60)
