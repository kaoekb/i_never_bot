# Dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p logs && chmod 777 logs
COPY . .
CMD ["python", "main.py"]
