from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, users, files
from app.db.session import engine
from app.models import user, file
import uvicorn

app = FastAPI(docs_url="/swagger", redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(files.router, prefix="/api/v1/files", tags=["files"])

# Создаём таблицы в базе данных, если они не существуют
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(user.Base.metadata.create_all)
        await conn.run_sync(file.Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
