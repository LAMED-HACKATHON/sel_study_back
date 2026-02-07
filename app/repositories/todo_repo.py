from datetime import date

from sqlalchemy import BigInteger, String, column, func, select, table
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.model.todos import Todo


class TodoRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_today_todos_by_user_id(self, user_id: int, target_date: date):
        t = aliased(Todo)
        s = table(
            "subjects",
            column("id", BigInteger),
            column("sub_name", String),
        )

        stmt = (
            select(
                t.id.label("todo_id"),
                t.title,
                t.content,
                t.status_yn,
                s.c.sub_name.label("subject_name"),
                t.todo_type,
                t.img_url1,
                t.img_url2,
                t.file_url1,
                t.file_url2,
                t.created_at,
            )
            .select_from(t)
            .join(s, t.subject_id == s.c.id)
            .where(
                t.user_id == user_id,
                func.date(t.created_at) <= target_date,
                t.end_time >= target_date,
            )
            .order_by(t.created_at.desc())
        )

        result = await self.db.execute(stmt)
        return result.all()


    async def get_today_todo_by_todo_id(self, todo_id: int):
        t = aliased(Todo)
        s = table(
            "subjects",
            column("id", BigInteger),
            column("sub_name", String),
        )

        stmt = (
            select(
                t.id.label("todo_id"),
                t.title,
                t.content,
                t.status_yn,
                s.c.sub_name.label("subject_name"),
                t.todo_type,
                t.img_url1,
                t.img_url2,
                t.file_url1,
                t.file_url2,
                t.created_at,
            )
            .select_from(t)
            .join(s, t.subject_id == s.c.id)
            .where(t.id == todo_id)
        )

        result = await self.db.execute(stmt)
        return result.one_or_none()