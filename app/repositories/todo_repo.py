from datetime import date

from sqlalchemy import BigInteger, String, column, delete, func, select, table, update
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
                t.writer_id,
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
                t.writer_id,
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

    async def insert_todos(self, todos: list[Todo]) -> None:
        self.db.add_all(todos)
        await self.db.flush()
        await self.db.commit()

    async def update_todo(self, todo_id: int, writer_id: int, items: dict):
        stmt = (
            update(Todo)
            .where(Todo.id == todo_id, Todo.writer_id == writer_id)
            .values(**items)
        )
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete_todo(self, todo_id: int, writer_id: int) -> None:
        stmt = delete(Todo).where(Todo.id == todo_id, Todo.writer_id == writer_id)
        await self.db.execute(stmt)
        await self.db.commit()