import telebot
import os

TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 Bangla Signal Bot is Live 24/7!")

print("Bot Running...")
bot.infinity_polling()
