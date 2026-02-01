import ssl
import os
from app.core.config import settings
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase

# =========================
# SSL Context (조건부)
# =========================
ssl_context = None

# Azure MySQL (호스트가 Azure 도메인인 경우) 또는 SSL이 필요한 경우
# 로컬 MySQL(localhost/127.0.0.1)은 SSL 불필요
if settings.MYSQL_HOST and settings.MYSQL_HOST not in ["localhost", "127.0.0.1"]:
    # Azure MySQL용 SSL 설정
    try:
        # Linux 경로 시도
        cert_path = "/etc/ssl/certs/ca-certificates.crt"
        if os.path.exists(cert_path):
            ssl_context = ssl.create_default_context(cafile=cert_path)
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED
        else:
            # Windows 또는 다른 환경: 시스템 기본 CA 사용
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = True
            ssl_context.verify_mode = ssl.CERT_REQUIRED
    except Exception:
        # SSL 설정 실패 시 None으로 설정 (로컬 MySQL은 SSL 불필요)
        ssl_context = None



# =========================
# Async Engine
# =========================
connect_args = {}
if ssl_context:
    connect_args["ssl"] = ssl_context

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,           # 풀 기본 크기
    max_overflow=settings.DB_MAX_OVERFLOW,     # 순간 트래픽 버퍼
    pool_timeout=settings.DB_POOL_TIMEOUT,     # 풀 대기 시간
    pool_recycle=settings.DB_POOL_RECYCLE,  
    connect_args=connect_args,  # SSL이 None이면 전달하지 않음
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
