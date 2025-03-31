from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.services.file_service import upload_audio_file, get_audio_files, delete_audio_file
from app.schemas.file import AudioFileResponse
from app.db.session import get_db
from app.db.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import get_current_user

router = APIRouter()


@router.post("/upload", response_model=AudioFileResponse)
async def upload_file(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    file_info = await upload_audio_file(file, db)
    return file_info


@router.get("/list", response_model=list[AudioFileResponse])
async def list_audio_files(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    audio_files = await get_audio_files(user, db)
    return audio_files


@router.delete("/delete/{file_id}")
async def delete_file(file_id: int, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Удаление аудиофайла пользователя.
    """
    success = await delete_audio_file(file_id, user, db)
    if not success:
        raise HTTPException(status_code=404, detail="File not found or unauthorized")
    return {"message": "File deleted successfully"}
