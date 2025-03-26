# 1. Используем официальный образ Python
FROM python:3.10-slim

# 2. Указываем рабочую директорию для контейнера
WORKDIR /app

# 3. Копируем requirements.txt в контейнер
COPY requirements.txt /app/

# 4. Устанавливаем зависимости через pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь проект в контейнер
COPY . /app

# 6. Указываем команду по умолчанию
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]