import telebot
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

CHAT_ID = "8178103030"

bot.send_message(CHAT_ID, "🔥 Test Signal Working!")
print("Message Sent")
