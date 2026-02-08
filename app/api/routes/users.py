from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.schemas.users import LoginRequest, LoginResponse, MenteeInfo
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
        samesite="lax",
    )

    return login_response

@router.post("/logout")
async def logout(session_id: str, user_id: int = Depends(get_current_user_id)):
    await http_session.invalidate(session_id)
    return{
        "success" : True
    }


@router.get("/mentee", response_model=list[MenteeInfo])
async def get_mentee(
    request: Request,
    user_id: int = Depends(get_current_user_id),
    user_service: UserService = Depends(get_user_service),
):
    print("router 진입")
    print(f"user_id -> {user_id}")
    print(f"method={request.method} url={request.url}")

    # 헤더/쿠키/쿼리
    print("headers ->", dict(request.headers))
    print("cookies ->", request.cookies)
    print("query_params ->", dict(request.query_params))

    # 바디(raw). GET은 보통 비어있습니다.
    body_bytes = await request.body()
    print("body(raw) ->", body_bytes.decode("utf-8", errors="replace") if body_bytes else "<empty>")

    return await user_service.get_mentee(user_id)

