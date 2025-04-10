FROM python:3.10
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создаем папку логов с правами
RUN mkdir -p logs && chmod 777 logs

# Копируем весь проект
COPY . .

# Удаляем лог при каждом запуске контейнера
CMD ["sh", "-c", "rm -f logs/bot.log && python main.py"]
