from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "Audio Service API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Настройка строки подключения или отдельных параметров
    DB_USER: str = 'user'
    DB_PASSWORD: str = 'password'
    DB_HOST: str = 'db'
    DB_PORT: int = '5232'
    DB_NAME: str = 'fastapi_db'

    # DATABASE_SQLITE = 'sqlite+aiosqlite:///data/db.sqlite3'
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    # Настройки аутентификации через Яндекс
    YANDEX_CLIENT_ID: str = ""
    YANDEX_CLIENT_SECRET: str = ""

    # Настройки токенов
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Путь для хранения файлов
    MEDIA_DIRECTORY: str = os.path.join(os.getcwd(), "storage")


# Инициализация настроек
settings = Settings()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


@app.get("/")
def root():
    return {"message": settings.PROJECT_NAME, "db_url": settings.get_db_url()}
