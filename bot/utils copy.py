# utils.py
import logging
from config import ADMIN_ID
from datetime import datetime
import re

def notify_admin(bot, message):
    """Отправляет сообщение админу о важном событии или ошибке."""
    try:
        bot.send_message(ADMIN_ID, f"🔔 Уведомление: {message}")
    except Exception as e:
        logging.error(f"Ошибка отправки уведомления админу: {e}")

def format_date(timestamp):
    """Преобразует timestamp в читаемый формат."""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def truncate_text(text, length=100):
    """Обрезает текст до указанной длины и добавляет '...' в конце, если он длинный."""
    return text[:length] + "..." if len(text) > length else text

def is_valid_url(url):
    """Проверяет, является ли строка валидным URL."""
    regex = re.compile(r'^(https?://)?(www\.)?[\w-]+(\.[a-z]{2,})+(/[\w-]*)*$')
    return re.match(regex, url) is not None
