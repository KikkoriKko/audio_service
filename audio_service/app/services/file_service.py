import aiofiles
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, HTTPException
from pathlib import Path
from app.models.file import AudioFile
from app.core.config import settings
from app.models.user import User

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