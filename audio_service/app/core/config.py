from fastapi import FastAPI
from pydantic_settings import BaseSettings
import os
from urllib.parse import urlparse


class Settings(BaseSettings):
    PROJECT_NAME: str = "Audio Service API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Получаем DATABASE_URL или отдельные параметры
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "audio_db")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))

    def get_db_url(self) -> str:
        """Возвращает строку подключения к БД"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    # Настройки аутентификации через Яндекс
    YANDEX_CLIENT_ID: str = os.getenv("YANDEX_CLIENT_ID", "")
    YANDEX_CLIENT_SECRET: str = os.getenv("YANDEX_CLIENT_SECRET", "")

    # Настройки токенов
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    MEDIA_DIRECTORY: str = os.path.join(os.getcwd(), "storage")

    class Config:
        env_file = ".env"
        extra = "allow"  # Разрешает дополнительные параметры


# Инициализация настроек
settings = Settings()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


@app.get("/")
def root():
    return {"message": settings.PROJECT_NAME, "db_url": settings.get_db_url()}
