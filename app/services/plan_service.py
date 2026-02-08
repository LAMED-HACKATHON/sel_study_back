from app.repositories.plan_repo import PlanRepository
from app.schemas.plans import PlanRequest, PlanResponse, PlanUpdateRequest


class PlanService:

    def __init__(self, plan_repo: PlanRepository) -> None:
        self.plan_repo = plan_repo


    async def create_planner(self, request: PlanRequest, user_id: int) -> PlanResponse:
        row = await self.plan_repo.get_plan_content_by_user_id(user_id, request.target_date)
        if row:
            return PlanResponse(id=row.id, plan_content=row.plan_content)

        plan = await self.plan_repo.create_plan(user_id, request.target_date)
        return PlanResponse(id=plan.id, plan_content=plan.plan_content)


    async def update_planner(self, request: PlanUpdateRequest, user_id: int) -> PlanResponse:
        plan = await self.plan_repo.update_plan(user_id, request.target_date, request.plan_content)
        return PlanResponse(id=plan.id, plan_content=plan.plan_content)

    

