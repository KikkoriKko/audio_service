# audio_service
# Документация по развертыванию сервиса и БД в Docker

## 1. Установка зависимостей
Перед началом убедитесь, что у вас установлены:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 2. Структура проекта
```
fastapi_audio_service/  
│── app/  
│   │── api/  
│   │   │── v1/  
│   │   │   │── endpoints/  
│   │   │   │   │── auth.py  # Авторизация через Яндекс  
│   │   │   │   │── users.py  # Управление пользователями  
│   │   │   │   │── files.py  # Работа с аудиофайлами  
│   │── core/  
│   │   │── config.py  # Конфигурация приложения  
│   │   │── security.py  # JWT и безопасность  
│   │── models/  
│   │   │── user.py  # Модель пользователя  
│   │   │── file.py  # Модель аудиофайла  
│   │── schemas/  
│   │   │── user.py  # Pydantic-схемы для пользователей  
│   │   │── file.py  # Pydantic-схемы для аудиофайлов  
│   │── services/  
│   │   │── auth_service.py  # Логика аутентификации  
│   │   │── file_service.py  # Работа с файлами  
│   │── db/  
│   │   │── session.py  # Подключение к БД  
│   │   │── base.py  # Базовые модели  
│   │   │── migrations/  # Миграции Alembic  
│   │── main.py  # Основной файл FastAPI  
│── storage/  # Локальное хранилище аудиофайлов  
│── .env  # Переменные окружения  
│── Dockerfile  # Образ для Docker  
│── docker-compose.yml  # Контейнеризация  
│── requirements.txt  # Python-зависимости  
│── README.md  # Документация  
```

## 3. Настройка переменных окружения
Создайте файл `.env` в корне проекта и укажите в нем:
```
POSTGRES_DB=fastapi_db
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=fastapi_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
YANDEX_CLIENT_ID=your_client_id
YANDEX_CLIENT_SECRET=your_client_secret
YANDEX_REDIRECT_URI=your_redirect_uri
```

## 4. Конфигурация Dockerfile
```dockerfile
# Используем Python 3.11
FROM python:3.11

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта
COPY . .

# Открываем порт и запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 5. Конфигурация docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:16
    restart: always
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  app:
    build: .
    depends_on:
      - db
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_HOST: db
      POSTGRES_PORT: 5432
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

volumes:
  postgres_data:
```

## 6. Запуск проекта в Docker
1. Соберите и запустите контейнеры:
   ```sh
   docker-compose up --build
   ```
2. Проверьте, что сервис работает:
   ```sh
   curl http://localhost:8000/docs
   ```

## 7. Выполнение миграций БД
Если используется Alembic, выполните миграции после первого запуска:
```sh
docker-compose exec app alembic upgrade head
```

## 8. Остановка и удаление контейнеров
Для остановки контейнеров:
```sh
docker-compose down
```
Для удаления всех данных БД:
```sh
docker volume rm fastapi_audio_service_postgres_data
```

