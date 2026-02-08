from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.append_content import AppendContent
from app.model.feedback import Feedback
from app.model.todos import Todo  # noqa: F401  # FK("todos.id") 메타데이터 등록용


class FeedbackRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_append_by_feedback_id(self, feedback_id: int) -> list[AppendContent]:
        stmt = (
            select(AppendContent)
            .where(AppendContent.feedback_id == feedback_id)
            .order_by(AppendContent.created_at.desc(), AppendContent.id.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_append(self, feedback_id: int) -> list[AppendContent]:
        append = AppendContent(feedback_id=feedback_id, content=None)
        self.db.add(append)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(append)
        return [append]

    async def insert_append(self, feedback_id: int) -> AppendContent:
        append = AppendContent(feedback_id=feedback_id, content=None)
        self.db.add(append)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(append)
        return append

    async def get_feedback_by_todo_id(self, todo_id: int):
        stmt = (
            select(
                Feedback.id,
                Feedback.todo_id,
                Feedback.content,
                Feedback.summary,
                Feedback.created_at
            )
            .where(Feedback.todo_id == todo_id)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.one_or_none()

    async def create_feedback(self, todo_id: int) -> Feedback:
        feedback = Feedback(todo_id=todo_id, content=None, summary=None)
        self.db.add(feedback)
        await self.db.flush()
        await self.db.commit()
        await self.db.refresh(feedback)
        return feedback

    async def update_feedback(self, todo_id: int, content: str | None, summary: str | None) -> Feedback:
        stmt = (
            select(Feedback)
            .where(Feedback.todo_id == todo_id)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        feedback = result.scalar_one_or_none()

        if feedback is None:
            feedback = Feedback(todo_id=todo_id, content=None, summary=None)
            self.db.add(feedback)
            await self.db.flush()

        feedback.content = content
        feedback.summary = summary
        await self.db.commit()
        await self.db.refresh(feedback)
        return feedback

    async def update_append(self, append_content_id: int, content: str | None) -> AppendContent:
        stmt = (
            select(AppendContent)
            .where(AppendContent.id == append_content_id)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        append = result.scalar_one_or_none()

        if append is None:
            raise ValueError("appendContentNotFound")

        append.content = content
        await self.db.commit()
        await self.db.refresh(append)
        return append