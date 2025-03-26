import signal  # Для работы с сигналами SIGINT
from multiprocessing import Process
from django.core.management.base import BaseCommand
from report.telegram_bot import bot
import psutil
import sys

# Флаг для отслеживания завершения процессов
TERMINATE = False


# Функция для запуска бота
def start_bot():
    print("Бот запущен!")
    try:
        bot.polling(timeout=10, long_polling_timeout=5, non_stop=True)
        print("[INFO]: Бот успешно запущен!")
    except Exception as e:
        print(f"[ERROR]: Произошла ошибка при запуске бота: {e}")


# Команда управления запуском бота и сервера Django
class Command(BaseCommand):
    help = "Запускает Telegram-бот и сервер Django одновременно."
    bot_process = None  # Переменная для отслеживания процесса

    def handle(self, *args, **options):
        global TERMINATE  # Используем общий флаг завершения
        self.stdout.write("[INFO]: Запускаем бот и сервер Django...")

        # Устанавливаем обработчик сигналов SIGINT
        signal.signal(signal.SIGINT, self.terminate_processes)

        # Проверка на уже запущенный процесс бота
        if not self.is_bot_running():
            self.bot_process = Process(target=start_bot, daemon=True)
            self.bot_process.start()
            self.stdout.write("[INFO]: Бот запущен! 🤖")
        else:
            self.stdout.write("[INFO]: Бот уже запущен. Пропускаем запуск.")

        # Запуск Django-сервера
        from django.core.management.commands.runserver import Command as RunserverCommand
        runserver = RunserverCommand()

        try:
            runserver.run_from_argv(["manage.py", "runserver", "--noreload", "127.0.0.1:8000"])
        except KeyboardInterrupt:
            # Завершение работы сервера
            self.terminate_processes(None, None)
            TERMINATE = True

        if TERMINATE:
            sys.exit(0)

    def is_bot_running(self):
        """Проверяем, работает ли бот, по имени процесса и сигнатуре cmdline."""
        for process in psutil.process_iter(attrs=["pid", "name", "cmdline"]):
            try:
                # Проверяем наличие процесса Python, связанного с ботом
                cmdline = process.info["cmdline"]
                if (
                        cmdline
                        and "python" in process.info["name"]  # Процессы Python
                        and any("start_bot" in arg for arg in cmdline)  # Сигнатура запуска бота
                ):
                    return True  # Процесс бота уже запущен
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False  # Процесса бота нет

    def terminate_processes(self, signum, frame):
        """Завершаем бот и сервер при нажатии SIGINT (CTRL+C)."""
        self.stdout.write("\n[INFO]: Завершаем процессы...")
        global TERMINATE
        TERMINATE = True

        # Завершаем процесс бота, если он активен
        if self.bot_process and self.bot_process.is_alive():
            self.stdout.write("[INFO]: Остановка процесса бота...")
            self.bot_process.terminate()
            self.bot_process.join()  # Ждём завершения бота

        self.stdout.write("[INFO]: Все процессы завершены. Выход.")
        sys.exit(0)
