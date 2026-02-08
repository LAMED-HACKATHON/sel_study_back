from fastapi import APIRouter, Depends

from app.api.deps import get_feedback_service
from app.schemas.feedpack import AppendCreateRequest, AppendCreateResponse, AppendDeleteRequest, AppendRequest, AppendResponse, AppendUpdateRequest, AppendUpdateResponse, FeedbackRequest, FeedbackResponse, FeedbackUpdateRequest
from app.services.feedback_service import FeedbackService

router = APIRouter()

# 피드백 조회 - 없으면 빈값 생성 -> 조회
@router.post("/", response_model=FeedbackResponse)
async def create_feedback(request: FeedbackRequest, feedback_service: FeedbackService = Depends(get_feedback_service)):
    return await feedback_service.create_feedback(request)

# 피드백 수정
@router.put("/update", response_model=FeedbackResponse)
async def update_feedback(request: FeedbackUpdateRequest, feedback_service: FeedbackService = Depends(get_feedback_service)):
    return await feedback_service.update_feedback(request)


# 추가내용 조회 - 없으면 빈값 생성 -> 페이징 로직
@router.post("/append", response_model=AppendResponse)
async def create_append(request: AppendRequest, feedback_service: FeedbackService = Depends(get_feedback_service)):
    return await feedback_service.create_append(request)

# 추가내용 추가
@router.post("/append/insert", response_model=AppendCreateResponse)
async def insert_append(request: AppendCreateRequest, feedback_service: FeedbackService = Depends(get_feedback_service)):
    return await feedback_service.insert_append(request)

# # 추가내용 수정
@router.put("/append/update", response_model=AppendUpdateResponse)
async def update_append(request: AppendUpdateRequest, feedback_service: FeedbackService = Depends(get_feedback_service)):
    return await feedback_service.update_append(request)

## 추가내용 삭제
@router.delete("/append/delete")
async def delete_append(request: AppendDeleteRequest, feedback_service: FeedbackService = Depends(get_feedback_service)):
    return await feedback_service.delete_append(request)
