from django.core.management.base import BaseCommand
import threading
import telebot

TOKEN = "7849588920:AAHZz2-8ED-fYdMQLCO9z0D2nJlTF_cxUaU"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, интегрированный в Django 😄.")


@bot.message_handler(commands=['setgroup'])
def send_group_id(message):
    bot.reply_to(message, f"ID этой группы 🆔: {message.chat.id}")


# Функция запуска бота
def start_bot():
    print("Бот запущен🤖!")
    bot.polling()


class Command(BaseCommand):
    help = "Запуск Telegram-бота"

    def handle(self, *args, **options):
        # Запускаем бота в отдельном потоке
        bot_thread = threading.Thread(target=start_bot)
        bot_thread.setDaemon(True)  # Устанавливаем поток как демонический
        bot_thread.start()

        # Теперь основной поток станет доступен для ввода других команд
        print("Бот запущен в фоновом режиме. Используйте `runserver` для запуска сервера.")
