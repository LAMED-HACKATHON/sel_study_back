from app.schemas.feedpack import FeedbackRequest, FeedbackResponse, FeedbackUpdateRequest
from app.repositories.feedback_repo import FeedbackRepository


class FeedbackService:

    def __init__(self, feedback_repo: FeedbackRepository) -> None:
        self.feedback_repo = feedback_repo

    async def create_feedback(self, request: FeedbackRequest) -> FeedbackResponse:
        row = await self.feedback_repo.get_feedback_by_todo_id(request.todo_id)
        if row:
            return FeedbackResponse(
                id=row.id,
                todo_id=row.todo_id,
                content=row.content,
                summary=row.summary,
                created_at=row.created_at
            )

        feedback = await self.feedback_repo.create_feedback(request.todo_id)
        return FeedbackResponse(
            id=feedback.id,
            todo_id=feedback.todo_id,
            content=feedback.content,
            summary=feedback.summary,
            created_at=feedback.created_at
        )

    async def update_feedback(self, request: FeedbackUpdateRequest) -> FeedbackResponse:
        feedback = await self.feedback_repo.update_feedback(request.todo_id, request.content, request.summary)
        return FeedbackResponse(
            id=feedback.id,
            todo_id=feedback.todo_id,
            content=feedback.content,
            summary=feedback.summary,
            created_at=feedback.created_at,
        )