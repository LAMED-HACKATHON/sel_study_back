from __future__ import annotations

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MatchMentee(Base):
    __tablename__ = "match_mentee"

    match_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    mentor_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)
    mentee_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=False)