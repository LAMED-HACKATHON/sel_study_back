from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


# getTodos
# req : 날짜, user_id
# resp : 할일 - todo_id, subject_name, title, content, status_yn, todo_type, img_url1, img_url2,
# file_url1, file_url2, created_at


class PlanRequest(BaseModel):
    target_date: date

class PlanUpdateRequest(PlanRequest):
    plan_content: str | None = None
    pass

class PlanResponse(BaseModel):
    id: int
    plan_content: str | None = None




