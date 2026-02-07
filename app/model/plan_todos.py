from __future__ import annotations

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PlanTodo(Base):
    __tablename__ = "plan_todos"

    plan_todos_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    plan_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("plans.id"), nullable=False)
    todo_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("todos.id", ondelete="CASCADE"),
        nullable=False,
    )

