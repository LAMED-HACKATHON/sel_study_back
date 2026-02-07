from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


# getTodos
# req : 날짜, user_id
# resp : 할일 - todo_id, subject_name, title, content, status_yn, todo_type, img_url1, img_url2,
#        file_url1, file_url2, created_at


class TodosRequest(BaseModel):
    target_date: date = Field(..., description="조회할 날짜")
    user_id: int = Field(..., ge=1)


class TodoResponse(BaseModel):
    todo_id: int
    title: str
    content: str | None = None
    status_yn: bool = False
    subject_name: str
    todo_type: Literal["homework", "routine"] | None = None
    img_url1: str | None = None
    img_url2: str | None = None
    file_url1: str | None = None
    file_url2: str | None = None
    created_at: datetime
