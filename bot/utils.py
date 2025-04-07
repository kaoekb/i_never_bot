import logging
from config import ADMIN_ID
from datetime import datetime, timedelta
import re
import random
import string

def notify_admin(bot, message):
    """Отправляет сообщение админу о важном событии или ошибке."""
    try:
        bot.send_message(ADMIN_ID, f"🔔 Уведомление: {message}")
    except Exception as e:
        logging.error(f"Ошибка отправки уведомления админу: {e}")

def format_date(timestamp):
    """Преобразует timestamp в читаемый формат."""
    if isinstance(timestamp, (int, float)):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    else:
        raise ValueError("Timestamp must be an integer or float.")

def truncate_text(text, length=100):
    """Обрезает текст до указанной длины и добавляет '...' в конце, если он длинный."""
    return text[:length] + "..." if len(text) > length else text

def is_valid_url(url):
    """Проверяет, является ли строка валидным URL."""
    regex = re.compile(r'^(https?://)?(www\.)?[\w-]+(\.[a-z]{2,})+(/[\w-]*)*$')
    return bool(re.match(regex, url))

def handle_error(error):
    """Обрабатывает ошибки и логирует их."""
    logging.error(f"Произошла ошибка: {error}")
    # Можно расширить обработку, например, отправить уведомление админу
    # notify_admin(bot, f"Ошибка: {error}")

def generate_random_string(length=10, chars=string.ascii_letters + string.digits):
    """Генерирует случайную строку заданной длины из символов, букв и цифр."""
    return ''.join(random.choice(chars) for _ in range(length))

def calculate_time_difference(date1, date2):
    """Вычисляет разницу между двумя датами и возвращает ее в виде строки."""
    if not isinstance(date1, datetime) or not isinstance(date2, datetime):
        raise ValueError("Both date1 and date2 must be datetime objects.")
    
    delta = date2 - date1
    return str(delta)

def add_days_to_date(date, days):
    """Добавляет указанное количество дней к дате."""
    if not isinstance(date, datetime):
        raise ValueError("date must be a datetime object.")
    
    return date + timedelta(days=days)

def remove_whitespace(text):
    """Удаляет все пробелы из строки."""
    return "".join(text.split())

def sanitize_input(text):
    """Удаляет нежелательные символы из строки."""
    # Пример: Убираем все символы, кроме букв, цифр и пробелов
    return re.sub(r'[^a-zA-Z0-9 ]', '', text)

def get_day_of_week(date):
    """Возвращает день недели для заданной даты."""
    if not isinstance(date, datetime):
        raise ValueError("date must be a datetime object.")
    
    return date.strftime('%A')

def convert_seconds_to_hms(seconds):
    """Конвертирует количество секунд в строку в формате 'часы:минуты:секунды'."""
    if not isinstance(seconds, (int, float)):
        raise ValueError("Input must be an integer or float.")
    
    return str(timedelta(seconds=seconds))

def is_email_valid(email):
    """Проверяет, является ли строка валидным email."""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(regex, email))

def is_phone_number_valid(phone_number):
    """Проверяет, является ли строка валидным номером телефона (пример для России)."""
    regex = r'^\+7\d{10}$'
    return bool(re.match(regex, phone_number))

def format_price(price):
    """Форматирует цену с разделением тысяч и добавлением валюты."""
    if not isinstance(price, (int, float)):
        raise ValueError("Price must be an integer or float.")
    
    return f"{price:,.2f} ₽"

