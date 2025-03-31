from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class AudioFile(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    path: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="files")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    yandex_user_id: Mapped[str | None] = mapped_column(String, unique=True, index=True, nullable=True)

    files = relationship("AudioFile", back_populates="owner")

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
