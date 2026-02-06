from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.users import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_by_email(self, email:str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()