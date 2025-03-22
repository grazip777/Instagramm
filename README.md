# Instagramm 😍

Простой веб-сайт, построенный с использованием [Django], для демонстрации базовых функций и структуры веб-приложений. Этот проект был создан специально для hackathon. 

## 📋 Описание

Сайт позволяет создавать посты, указывая авторов и присваивая хэштеги. Он поддерживает взаимодействие с API и может быть протестирован с использованием Postman.

## 🚀 Основные технологии

- **Python** — язык для разработки.
- **Django** — фреймворк для создания веб-приложений.
- **Django REST Framework** — для работы с API.

## 🛠 Установка и запуск
### 1. Клонируйте проект и установите зависимости:

```bash
git clone https://github.com/grazip777/instagramm.git
cd instagramm
pip install -r requirements.txt
```

### 2. Выполните миграции базы данных:
```bash
python manage.py migrate
```

### 3. Запустите локальный сервер разработчика:
```bash
python manage.py runserver
```

В результате вы увидите сообщение:
```plaintext
Starting development server at http://127.0.0.1:8000/
```

Скопируйте этот адрес и откройте его в браузере или используйте его в Postman для тестирования API.

## 📌 Примеры API-эндпоинтов (для Postman)

- **Получение списка постов:**
  ```
  GET /posts/
  ```
- **Создание нового поста:**
  ```
  POST /posts/
  Body (JSON):
  {
      "title": "My first post",
      "content": "Hello world! #welcome"
  }
  ```
- **Поиск постов по хэштегу:**
  ```
  GET /posts/hashtag/{hashtag_name}/
  ```
- **Пример ответа (JSON):**
  ```json
  [
      {
          "id": 1,
          "title": "My first post",
          "content": "Hello world! #welcome",
          "author": "username",
          "hashtags": ["welcome"]
      }
  ]
  ```

Теперь вы готовы работать с приложением! 🎉