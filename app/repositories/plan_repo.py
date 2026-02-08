from __future__ import annotations

from datetime import date, datetime, time

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.model.plans import Plan


class PlanRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_plan_content_by_user_id(self, user_id: int, target_date: date):
        stmt = (
            select(Plan.id, Plan.plan_content)
            .where(Plan.user_id == user_id, func.date(Plan.created_at) == target_date)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.one_or_none()

    async def create_plan(self, user_id: int, target_date: date, plan_content: str | None = None) -> Plan:
        plan = Plan(user_id=user_id, plan_content=None, created_at=datetime.combine(target_date, time.min))
        plan.plan_content = plan_content
        self.db.add(plan)
        await self.db.flush()
        await self.db.commit()
        return plan

    async def update_plan(self, user_id: int, target_date: date, plan_content: str | None) -> Plan:
        stmt = (
            select(Plan)
            .where(Plan.user_id == user_id, func.date(Plan.created_at) == target_date)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        plan = result.scalar_one_or_none()

        plan.plan_content = plan_content
        await self.db.commit()
        return plan