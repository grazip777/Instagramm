# report/utils.py
import requests

API_TOKEN = "7849588920:AAHZz2-8ED-fYdMQLCO9z0D2nJlTF_cxUaU"
SPAM_CHAT_ID = "-4720065914"  # Спам
FRAUD_CHAT_ID = "-4769114028" # Мошенничество
BAG_CHAT_ID = "-4736988210" # Баг
API_URL = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"

# Отправка сообщение на телеграмм
def send_message(text, category):
    try:
        if category == "Спам":
            response = requests.post(API_URL, data={"chat_id": SPAM_CHAT_ID, "text": text})
            response.raise_for_status()
        elif category == "Мошейнечество":
            response = requests.post(API_URL, data={"chat_id": FRAUD_CHAT_ID, "text": text})
            response.raise_for_status()
        elif category == "Баг":
            response = requests.post(API_URL, data={"chat_id": BAG_CHAT_ID, "text": text})
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке сообщения: {e}")
