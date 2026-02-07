from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class UserEmailPassword(BaseModel):
    email: str = Field(..., min_length=1, max_length=30)
    password: str = Field(..., min_length=1, max_length=128)


class LoginRequest(UserEmailPassword):
    role: Literal["mentee", "mentor"]

class LoginResponse(BaseModel):
    success: bool = Field(...)
    username: str
    name: str
    school_name: str | None = None
    birth_date: date | None = None
    role: Literal["mentee", "mentor"]
    # profile_img: str


class MenteeInfo(BaseModel):
    mentee_id: int
    name: str
    school_name: str | None = None
    birth_date: date | None = None