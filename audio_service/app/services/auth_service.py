import httpx
from sqlalchemy.future import select
from app.db.models import User
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

YANDEX_OAUTH_URL = "https://oauth.yandex.ru/token"
YANDEX_USERINFO_URL = "https://login.yandex.ru/info"


async def authenticate_user(code: str, db: AsyncSession) -> User | None:
    """
    Аутентификация пользователя через Яндекс OAuth
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                YANDEX_OAUTH_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": settings.YANDEX_CLIENT_ID,
                    "client_secret": settings.YANDEX_CLIENT_SECRET,
                }
            )
            response.raise_for_status()  # Генерирует исключение для HTTP ошибок
        except httpx.HTTPStatusError as e:
            # Логирование ошибки при HTTP запросе
            print(f"HTTP Error: {e}")
            return None
        except httpx.RequestError as e:
            # Логирование ошибок запросов
            print(f"Request Error: {e}")
            return None

        data = response.json()
        access_token = data.get("access_token")
        if not access_token:
            print("Access token is missing in response")
            return None

    # Получаем информацию о пользователе с использованием access_token
    async with httpx.AsyncClient() as client:
        try:
            user_info = await client.get(
                YANDEX_USERINFO_URL,
                headers={"Authorization": f"OAuth {access_token}"}
            )
            user_info.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error fetching user info: {e}")
            return None
        except httpx.RequestError as e:
            print(f"Request Error fetching user info: {e}")
            return None

    user_data = user_info.json()
    yandex_user_id = user_data.get("id")

    # Проверка существования пользователя в базе данных
    result = await db.execute(select(User).filter(User.yandex_user_id == yandex_user_id))
    user = result.scalars().first()

    if not user:
        # Создаем нового пользователя, если он не найден
        user = User(username=user_data.get("display_name"), yandex_user_id=yandex_user_id)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """
    Получение текущего пользователя из JWT токена
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user
