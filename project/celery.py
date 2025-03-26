# project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

# Загружаем настройки для Celery из settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическая регистрация задач
app.autodiscover_tasks()
