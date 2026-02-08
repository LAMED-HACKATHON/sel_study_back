from __future__ import annotations

import ssl
from typing import Any, Iterable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


def _coerce_database_url(value: Any) -> str:

    if isinstance(value, str):
        return value

    if isinstance(value, set):
        if not value:
            raise ValueError("SQLALCHEMY_DATABASE_URL is empty.")
        return str(next(iter(value)))

    if isinstance(value, dict):
        if not value:
            raise ValueError("SQLALCHEMY_DATABASE_URL is empty.")
        return str(next(iter(value.values())))

    if isinstance(value, (list, tuple)):
        if not value:
            raise ValueError("SQLALCHEMY_DATABASE_URL is empty.")
        return str(value[0])

    return str(value)


def _build_connect_args() -> dict[str, Any]:


    host = (settings.MYSQL_HOST or "").strip().lower()
    if host in {"localhost", "127.0.0.1"}:
        return {}


    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = True
    ssl_context.verify_mode = ssl.CERT_REQUIRED
    return {"ssl": ssl_context}


DATABASE_URL = _coerce_database_url(settings.SQLALCHEMY_DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=_build_connect_args(),
)


# =========================
# Async Session Factory
# =========================
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# =========================
# Dependency (FastAPI)
# =========================
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# =========================
# Declarative Base
# =========================
class Base(DeclarativeBase):
    pass
