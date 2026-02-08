from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id, get_plan_service
from app.schemas.plans import PlanRequest, PlanResponse, PlanUpdateRequest
from app.services.plan_service import PlanService


router = APIRouter()


# 플래너 조회 및 생성 (없으면 생성 후 반환)
@router.post("/", response_model=PlanResponse)
async def create_planner(request: PlanRequest, user_id: int = Depends(get_current_user_id), plan_service: PlanService = Depends(get_plan_service)):
    return await plan_service.create_planner(request, user_id)


# 플래너 수정
@router.put("/update", response_model=PlanResponse)
async def update_planner(request: PlanUpdateRequest, user_id: int = Depends(get_current_user_id), plan_service: PlanService = Depends(get_plan_service)):
    return await plan_service.update_planner(request, user_id)