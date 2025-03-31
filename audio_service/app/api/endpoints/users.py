from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.db.models import User
from app.core.security import get_password_hash, create_access_token, verify_password
from app.services.auth_service import get_current_user, get_admin_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await User.get_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_in.password)
    new_user = await User.create(db, username=user_in.username, hashed_password=hashed_password)
    return new_user

@router.post("/token")
async def login_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await User.authenticate(db, username=user_in.username, password=user_in.password, verify_func=verify_password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}

@router.patch("/update", response_model=UserResponse)
async def update_user(
        user_update: UserUpdate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    """
    Обновление данных пользователя (например, смена пароля).
    """
    if user_update.password:
        user_update.hashed_password = get_password_hash(user_update.password)
    updated_user = await User.update_user(db, user_id=current_user.id, user_update=user_update)
    return updated_user

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, admin: User = Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    """
    Удаление пользователя. Только суперпользователь может удалять других.
    """
    success = await User.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
