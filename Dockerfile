FROM python:3.10
WORKDIR /app
ENV $(cat .env | xargs)


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p logs && chmod 777 logs

COPY . .

# Удаляем лог при каждом запуске контейнера
CMD ["sh", "-c", "rm -f logs/bot.log && python main.py"]
