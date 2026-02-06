from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.schemas.users import LoginRequest, LoginResponse
from app.api.deps import get_current_user_id, get_user_service
from app.core.http_session import http_session
from app.services.user_service import UserService

router = APIRouter()



@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, response: Response, user_service: UserService = Depends(get_user_service)):

    try:
        session_id, login_response = await user_service.login(request)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 비밀번호가 일치하지 않습니다",
        )
    response.set_cookie(
        key = "session_id",
        value = session_id,
        httponly=True,
        secure=False,
        samesite="Lax",
    )

    return login_response

@router.post("/logout")
async def logout(session_id: str, user_id: int = Depends(get_current_user_id)):
    await http_session.invalidate(session_id)
    return{
        "success" : True
    }

    

