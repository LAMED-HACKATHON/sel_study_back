from datetime import datetime

from pydantic import BaseModel



# todo_id

class FeedbackRequest(BaseModel):
    todo_id: int

class FeedbackUpdateRequest(FeedbackRequest):
    content: str | None = None
    summary: str | None = None
    pass

class FeedbackResponse(BaseModel):
    id: int
    todo_id: int
    content: str | None = None
    summary: str | None = None
    created_at: datetime

class AppendRequest(BaseModel):
    feedback_id: int
    page_number: int = 1

class AppendResponse(BaseModel):
    id: int
    total: int
    content: str | None = None

class AppendUpdateRequest(BaseModel):
    append_content_id: int
    content: str | None = None


# class AppendUpdateResponse(BaseModel):


