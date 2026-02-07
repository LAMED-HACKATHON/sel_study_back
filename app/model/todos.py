from __future__ import annotations

from datetime import date, datetime
from math import fabs

from sqlalchemy import BigInteger, Boolean, Date, DateTime, Enum, ForeignKey, String, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    subject_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("subjects.id"), nullable=False)
    todo_type: Mapped[str | None] = mapped_column(
        Enum("homework", "routine", name="todo_type"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    status_yn: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("0"))
    content: Mapped[str | None] = mapped_column(Text, nullable=True)

    img_url1: Mapped[str | None] = mapped_column(String(255), nullable=True)
    img_url2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_url1: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_url2: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    
    )

    end_time : Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

