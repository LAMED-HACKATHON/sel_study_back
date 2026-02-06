from __future__ import annotations
from datetime import date, datetime
from enum import Enum as PyEnum
from sqlalchemy import BigInteger, Date, DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class UserRole(str, PyEnum):
    mentee = "mentee"
    mentor = "mentor"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(10), nullable=False)
    school_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

