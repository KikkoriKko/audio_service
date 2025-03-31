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
│   │── schemas/  
│   │   │── user.py  # Pydantic-схемы для пользователей  
│   │   │── file.py  # Pydantic-схемы для аудиофайлов  
│   │── services/  
│   │   │── auth_service.py  # Логика аутентификации  
│   │   │── file_service.py  # Работа с файлами  
│   │── db/  
│   │   │── session.py  # Подключение к БД  
│   │   │── base.py  # Базовые модели  
│   │   │── mоdels/  # модели  
│   │── main.py  # Основной файл FastAPI 
│── migrations/  # Миграции Alembic 
│── storage/  # Локальное хранилище аудиофайлов  
│── .env  # Переменные окружения  
│── Dockerfile  # Образ для Docker  
│── docker-compose.yml  # Контейнеризация  
│── requirements.txt  # Python-зависимости  
│── Documentation.md  # Документация  
```

## 3. Настройка переменных окружения
Создайте файл `.env` в корне проекта и укажите в нем:
```
DATABASE_URL = postgresql+asyncpg://user:password@db:5432/fastapi_db
SECRET_KEY = mysecretkey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
DB_PORT=5432
DB_NAME=fastapi_db
DB_USER=user
DB_PASSWORD=password
```

## 4. Конфигурация Dockerfile
```dockerfile
# Используем Python 3.10
FROM python:3.10
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
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - .env
  db:
    image: postgres
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: fastapi_db
    ports:
      - "5432:5432"
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
## 7. Проверка работы API в swagger
```
Откройте свагер по ссылке из терминала докера 

Авторизуйтесь

Проверьте работу апи 
```

