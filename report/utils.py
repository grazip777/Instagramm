from telebot import TeleBot

TOKEN = "7849588920:AAHZz2-8ED-fYdMQLCO9z0D2nJlTF_cxUaU"
GROUP_ID = -1002432586762
bot = TeleBot(TOKEN)


def send_to_telegram(data):
    try:
        message = (
            f"📝 *Новая жалоба:*\n"
            f"🔹 *ID:* {data.get('id')}\n"
            f"👤 *От пользователя:* {data.get('user')}\n"
            f"🔸 *На пользователя:* {data.get('to')}\n"
            f"❓ *Категория:* {data.get('reason')}\n"
            f"💬 *Описание:* {data.get('description')}\n"
            f"📅 *Создано:* {data.get('created_at')}\n"
        )

        bot.send_message(chat_id=GROUP_ID, text=message, parse_mode="Markdown")
    except Exception as e:
        print(f"Ошибка отправки сообщения в Telegram: {e}")
