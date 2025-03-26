# users/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User


@shared_task
def send_email_to_all_users():
    """
    Отправляет email всем пользователям.
    """
    users = User.objects.all()  # Получаем всех пользователей
    for user in users:
        # Рассылаем письма каждому
        send_mail(
            subject='Привет!',
            message='Это автоматическое сообщение, отправляемое каждые 5 минут.',
            from_email='admin@example.com',  # Ваш email отправителя
            recipient_list=[user.email],  # Email получателя
            fail_silently=False,  # True, если хотите игнорировать ошибки
        )
    return f"Сообщения отправлены {len(users)} пользователям."
