from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from alembic import context
from app.core.config import settings
import asyncio

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None  # Ваши модели здесь

SQLALCHEMY_DATABASE_URL = config.get_main_option("sqlalchemy.url")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

def run_migrations_online():
    connectable = create_async_engine(settings.get_db_url(), echo=True)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Создаем асинхронное подключение
    async with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        # Начинаем миграцию
        with context.begin_transaction():
            await context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()  # Синхронный режим
else:
    asyncio.run(run_migrations_online())  # Асинхронный режим
