from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker)
from app.core.config import settings

SQLALCHEMY_DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=SQLALCHEMY_DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    async with async_session_maker() as session:
        yield session
