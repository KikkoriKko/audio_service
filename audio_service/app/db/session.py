from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings

# Создаем асинхронный движок для работы с PostgreSQL
SQLALCHEMY_DATABASE_URL = settings.get_db_url()

# Создаем движок для асинхронных операций
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    future=True
)

# Создаем сессию для асинхронного использования
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    """
    Функция, которая используется для получения текущей сессии базы данных.
    """
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            print(f"Ошибка SQLAlchemy: {e}")
            raise e
        finally:
            await session.close()
