import telebot

API_TOKEN = "7849588920:AAHZz2-8ED-fYdMQLCO9z0D2nJlTF_cxUaU"
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, интегрированный в Django 🤖.")


@bot.message_handler(commands=['setgroup'])
def send_group_id(message):
    bot.reply_to(message, f"ID этой группы: {message.chat.id}")


@bot.message_handler(func=lambda m: m and m.text)
def echo_all(message):
    print(f"Получено сообщение: {message.text}")
    bot.reply_to(message, f"Вы написали: {message.text}")
