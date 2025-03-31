from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker)
from app.core.config import settings

# Создаем асинхронный движок для работы с PostgreSQL
SQLALCHEMY_DATABASE_URL = settings.get_db_url()

# Создаем движок для асинхронных операций
engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL)

# Создаем сессию для асинхронного использования
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session_maker() as session:
        yield session