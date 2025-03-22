import requests

TELEGRAM_BOT_TOKEN = '7849588920:AAHZz2-8ED-fYdMQLCO9z0D2nJlTF_cxUaU'
TELEGRAM_CHAT_ID = '@your_channel_or_chat_id'


def send_to_telegram(data):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    message_text = f"<b>Новая заявка</b>\n\n<pre>{data}</pre>"

    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message_text,
        'parse_mode': 'HTML'
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        print(f"Ошибка отправки в Telegram: {response.text}")

    return response.status_code
