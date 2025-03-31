from pydantic import BaseModel
from datetime import datetime


class FileBase(BaseModel):
    name: str
    path: str


class FileCreate(FileBase):
    pass


class AudioFileResponse(FileBase):
    id: int
    owner_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True
