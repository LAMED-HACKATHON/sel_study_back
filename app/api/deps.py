from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

from app.services.user_service import UserService
from app.repositories.user_repo import UserRepository

from app.core.http_session import http_session


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:

    user_repo = UserRepository(db)
    return UserService(user_repo)


async def get_current_user_id(session_id: str | None = Cookie(default=None),):
    if not session_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id = await http_session.get(session_id)
    
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user_id
