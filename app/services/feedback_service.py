from app.schemas.feedpack import AppendCreateRequest, AppendCreateResponse, AppendDeleteRequest, AppendRequest, AppendResponse, AppendUpdateRequest, AppendUpdateResponse, FeedbackRequest, FeedbackResponse, FeedbackUpdateRequest
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

    async def create_append(self, request: AppendRequest) -> AppendResponse:
        rows = []
        rows = await self.feedback_repo.get_append_by_feedback_id(request.feedback_id)

        if not rows:
            rows = await self.feedback_repo.create_append(request.feedback_id)

        if rows:
            page_number = request.page_number - 1
            row = rows[page_number]

            return AppendResponse(
                id=row.id,
                total=len(rows),
                content=row.content
            )


    async def update_append(self, request: AppendUpdateRequest) -> AppendUpdateResponse:
        append = await self.feedback_repo.update_append(request.append_content_id, request.content)
        return AppendUpdateResponse(
            feedback_id=append.feedback_id,
            content=append.content
        )

    async def insert_append(self, request: AppendCreateRequest) -> AppendCreateResponse:
        append = await self.feedback_repo.insert_append(request.feedback_id)
        return AppendCreateResponse(
            id=append.id,
            content=append.content
        )

    async def delete_append(self, request: AppendDeleteRequest) -> None:
        await self.feedback_repo.delete_append(request.id)