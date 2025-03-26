import telebot
import os

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Получаем токен из переменной окружения


class TelegramBot:
    def __init__(self, api_token=None):
        self.api_token = api_token or API_TOKEN
        self.bot = telebot.TeleBot(self.api_token)

    def send_message(self, chat_id, text):
        """
        Отправляет сообщение в Telegram чат.
        """
        return self.bot.send_message(chat_id, text)

    def handle_update(self, update):
        """
        Обрабатывает обновление Telegram от вебхука.
        """
        # В этом методе можно реализовать логику обработки обновлений
        print(f"Обновление: {update}")
        return "Processed"

    def start_bot(self):
        """
        Запускает цикл получения и обработки сообщений.
        """
        print("Бот запущен. Ожидаю сообщений...")
        self.bot.polling()


# Пример использования
if __name__ == "__main__":
    tg_bot = TelegramBot(api_token="ваш_тестовый_токен")
    tg_bot.start_bot()
