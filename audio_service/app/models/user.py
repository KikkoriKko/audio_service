from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    yandex_user_id = Column(String, unique=True, index=True, nullable=True)  # Поле для OAuth

    files = relationship("AudioFile", back_populates="owner")  # Связь с файлами

    @classmethod
    async def get_by_username(cls, db: AsyncSession, username: str):
        query = select(cls).where(cls.username == username)
        result = await db.execute(query)
        return result.scalars().first()

    @classmethod
    async def authenticate(cls, db: AsyncSession, username: str, password: str, verify_func):
        user = await cls.get_by_username(db, username)
        if user and verify_func(password, user.hashed_password):
            return user
        return None

    @classmethod
    async def create(cls, db: AsyncSession, username: str, hashed_password: str, yandex_user_id: str = None):
        new_user = cls(username=username, hashed_password=hashed_password, yandex_user_id=yandex_user_id)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user