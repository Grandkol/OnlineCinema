from core.config import settings
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Создаём базовый класс для будущих моделей
Base = declarative_base()

# dsn = f'postgresql+asyncpg://{settings.user}:{settings.password}@{settings.host}:{settings.port}/{settings.db_name}'
dsn = f'postgresql+asyncpg://postgres:123@theatre-db:5432/postgres'
engine = create_async_engine(dsn, echo=True, future=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

