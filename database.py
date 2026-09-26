import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool


def _normalize_url(url: str) -> str:
    """Ensure the URL uses the asyncpg dialect prefix."""
    if url.startswith("postgresql://"):
        url = "postgresql+asyncpg://" + url[len("postgresql://"):]
    return url


DATABASE_URL = _normalize_url(
    os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/real_estate_db",
    )
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    poolclass=NullPool,
)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
