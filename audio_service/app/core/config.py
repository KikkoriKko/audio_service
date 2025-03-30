from fastapi import FastAPI
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "Audio Service API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Настройка строки подключения или отдельных параметров
    DATABASE_URL: str
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "fastapi_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    def get_db_url(self) -> str:
        """Возвращает строку подключения к БД"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    # Настройки аутентификации через Яндекс
    YANDEX_CLIENT_ID: str = ""
    YANDEX_CLIENT_SECRET: str = ""

    # Настройки токенов
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Путь для хранения файлов
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
