from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.schemas.users import LoginRequest, LoginResponse, MenteeInfo
from app.api.deps import get_current_user_id, get_user_service
from app.core.http_session import http_session
from app.services.user_service import UserService

router = APIRouter()



@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    response: Response,
    http_request: Request,
    user_service: UserService = Depends(get_user_service),
):

    try:
        session_id, login_response = await user_service.login(login_data)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="아이디 비밀번호가 일치하지 않습니다",
        )
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="none",
    )
    print(f"method={http_request.method}")
    print(f"url={http_request.url}")  # 전체 URL
    print(f"base_url={http_request.base_url}")  # 스킴+호스트+포트
    print(f"path={http_request.url.path}")
    print(f"query={http_request.url.query}")
    print(f"host={http_request.headers.get('host')}")
    print(f"origin={http_request.headers.get('origin')}")
    print(f"referer={http_request.headers.get('referer')}")
    print("headers ->", dict(http_request.headers))
    print("cookie header(raw) ->", http_request.headers.get("cookie"))
    print("cookies(parsed) ->", http_request.cookies)

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
    print(f"method={request.method}")
    print(f"url={request.url}")          # 전체 URL
    print(f"base_url={request.base_url}")# 스킴+호스트+포트
    print(f"path={request.url.path}")
    print(f"query={request.url.query}")
    print(f"host={request.headers.get('host')}")
    print(f"origin={request.headers.get('origin')}")
    print(f"referer={request.headers.get('referer')}")
    print("headers ->", dict(request.headers))
    print("cookie header(raw) ->", request.headers.get("cookie"))
    print("cookies(parsed) ->", request.cookies)

    return await user_service.get_mentee(user_id)

