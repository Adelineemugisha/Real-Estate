import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def _normalize_url(url: str) -> str:

    if url.startswith("postgresql://"):
        url = "postgresql+asyncpg://" + url[len("postgresql://"):]

    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    query_params.pop("channel_binding", None)
    query_params.pop("sslmode", None)

    new_query = urlencode(query_params, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


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
