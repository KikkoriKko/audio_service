FROM python:3.9-slim

# Установка зависимостей
WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Запуск FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
