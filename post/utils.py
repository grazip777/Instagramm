import re


def extract_hashtags(text):
    """
    Функция для извлечения хэштегов из текста.
    """
    return set(part[1:] for part in text.split() if part.startswith('#'))
