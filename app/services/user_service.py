
import uuid
from app.repositories.user_repo import UserRepository
from app.schemas.users import LoginRequest, LoginResponse, MenteeInfo
from app.core.http_session import http_session


class UserService:

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    # 사용자 로그인
    async def login(self, request: LoginRequest) -> tuple[str, LoginResponse]:

        user = await self.user_repo.find_by_email(request.email)
        if not user:
            raise ValueError("usersValueError")

        if user.password != request.password:
            raise ValueError("비밀번호 불일치")
        
        session_id = str(uuid.uuid4())

        await http_session.set(
            session_id,
            user.id,
            ttl_minutes = 60
        )

        response = LoginResponse(
            success=True,
            username=user.username,
            name=user.name,
            role=getattr(user.role, "value", user.role),
            school_name=getattr(user, "school_name", None),
            birth_date=getattr(user, "birth_date", None),
        )

        return session_id, response

    async def logout(self, session_id: str):
        await http_session.invalidate(session_id)

    # 학생 목록 조회
    async def get_mentee(self, user_id: int) -> list[MenteeInfo]:
        
        mentees = await self.user_repo.get_mentees_by_mentor_id(user_id)

        result = []
        for mentee_id, name, school_name, birth_date in mentees:
            result.append(
                MenteeInfo(
                    mentee_id=mentee_id,
                    name=name,
                    school_name=school_name,
                    birth_date=birth_date,
                )
            )
        return result