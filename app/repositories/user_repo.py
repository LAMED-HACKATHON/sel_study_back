from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.model.users import User
from app.model.match_mentee import MatchMentee


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def find_by_email(self, email:str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()


    async def get_mentees_by_mentor_id(self, mentor_id: int):

        mentee = aliased(User)
        stmt = (
            select(mentee.id, mentee.name, mentee.school_name, mentee.birth_date)
            .select_from(MatchMentee)
            .join(mentee, MatchMentee.mentee_id == mentee.id)
            .where(MatchMentee.mentor_id == mentor_id)
        )

        result = await self.db.execute(stmt)
        return result.all()
        