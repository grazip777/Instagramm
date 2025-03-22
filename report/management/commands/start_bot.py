import telebot
from django.core.management.base import BaseCommand

# Замените 'ВАШ_ТОКЕН' на токен от BotFather
TOKEN = "7849588920:AAHZz2-8ED-fYdMQLCO9z0D2nJlTF_cxUaU"
bot = telebot.TeleBot(TOKEN)


# Определяем команды бота
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, интегрированный в Django 😄.")


@bot.message_handler(commands=['setgroup'])
def send_group_id(message):
    bot.reply_to(message, f"ID этой группы: {message.chat.id}")


class Command(BaseCommand):
    help = "Запуск Telegram-бота"

    def handle(self, *args, **options):
        print("Бот запущен!")
        bot.polling()

# @bot.message_handler(content_types=['text'])
# def get_chat_id(message):
#     # Выводим ID чата (супергруппы) в консоль
#     print(f"Chat ID (для супергруппы): {message.chat.id}")
#     bot.reply_to(message, f"ID этого чата: {message.chat.id}")
