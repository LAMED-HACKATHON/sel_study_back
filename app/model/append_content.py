from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AppendContent(Base):
    __tablename__ = "append_content"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    feedback_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("feedback.id", ondelete="CASCADE"),
        nullable=False,
    )

    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

