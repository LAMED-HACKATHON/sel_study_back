from fastapi import APIRouter, Depends

from app.api.deps import get_todo_service
from app.schemas.todos import TodoResponse, TodosRequest
from app.services.todo_service import TodoService


router = APIRouter()


# 학생의 당일 할일 리스트 불러오기
@router.get("/today/list", response_model=list[TodoResponse])
async def get_today_todos(request: TodosRequest = Depends(), todo_service: TodoService = Depends(get_todo_service)):

    return await todo_service.get_today_todos(request)

# todo_id -> todo_info
@router.get("/today", response_model=TodoResponse)
async def get_today_todo(todo_id: int, todo_service: TodoService = Depends(get_todo_service)):

    return await todo_service.get_today_todo(todo_id)


# 할일 등록

# 할일 수정

# 할일 삭제



