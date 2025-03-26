from __future__ import absolute_import, unicode_literals

# Это гарантирует, что при импорте Django также загружается Celery
from .celery import app as celery_app

__all__ = ['celery_app']
