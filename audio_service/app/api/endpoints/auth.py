from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth_service import authenticate_user, get_current_user
from app.schemas.user import UserResponse
from app.core.security import create_access_token
from app.db.session import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login", response_model=UserResponse)
async def login_with_yandex(code: str, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(code, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id)})  # Используем `sub`
    return {"user": user, "access_token": access_token}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: UserResponse = Depends(get_current_user)):
    return current_user
