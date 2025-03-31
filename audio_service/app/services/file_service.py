import aiofiles
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException
from pathlib import Path
import os
from app.db.models import AudioFile, User
from app.core.config import settings

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".ogg"}


async def upload_audio_file(file: UploadFile, db: AsyncSession):
    """
    Загрузка аудиофайла в локальное хранилище и сохранение данных в базе данных
    """
    ext = Path(file.filename).suffix
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file format. Only MP3, WAV, OGG are allowed.")

    file_location = Path(settings.MEDIA_DIRECTORY) / file.filename
    async with aiofiles.open(file_location, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            await f.write(chunk)

    new_file = AudioFile(name=file.filename, path=str(file_location))
    db.add(new_file)
    await db.commit()
    await db.refresh(new_file)
    return new_file


async def get_audio_files(user: User, db: AsyncSession):
    """
    Получение всех аудиофайлов, загруженных пользователем
    """
    result = await db.execute(select(AudioFile).filter(AudioFile.owner_id == user.id))
    return result.scalars().all()


async def delete_audio_file(file_id: int, user: User, db: AsyncSession) -> bool:
    """
    Удаление аудиофайла пользователя из базы данных и локального хранилища
    """
    result = await db.execute(select(AudioFile).filter(AudioFile.id == file_id, AudioFile.owner_id == user.id))
    audio_file = result.scalar_one_or_none()

    if not audio_file:
        return False  # Файл не найден или не принадлежит пользователю

    # Удаление файла из локального хранилища
    file_path = Path(audio_file.path)
    if file_path.exists():
        os.remove(file_path)

    # Удаление записи из базы данных
    await db.delete(audio_file)
    await db.commit()
    return True
