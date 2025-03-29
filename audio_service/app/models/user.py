from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    yandex_user_id = Column(String, unique=True, index=True, nullable=True)  # Поле для OAuth

    files = relationship("AudioFile", back_populates="owner")  # Связь с файлами

    @classmethod
    async def get_by_email(cls, db, email):
        result = await db.execute(select(cls).filter(cls.email == email))
        return result.scalars().first()

    @classmethod
    async def authenticate(cls, db, email, password, verify_func):
        user = await cls.get_by_email(db, email)
        if user and verify_func(password, user.hashed_password):
            return user
        return None
