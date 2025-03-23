import requests

API_TOKEN = "7849588920:AAHZz2-8ED-fYdMQLCO9z0D2nJlTF_cxUaU"
CHAT_ID = "2143828594"
API = "https://api.telegram.org/bot"
method = API + API_TOKEN + "/sendMessage"

def send_message(text):
    req = requests.post(method, data={
        "chat_id": CHAT_ID,
        "text": text
    })