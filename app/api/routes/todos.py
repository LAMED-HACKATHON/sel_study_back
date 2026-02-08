from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id, get_todo_service
from app.schemas.todos import TodoInsertReqeust, TodoResponse, TodoSuccessResponse, TodosRequest, TodoUpdateRequest
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
@router.post("/insert", response_model=TodoSuccessResponse)
async def insert_todos(request: TodoInsertReqeust, user_id: int = Depends(get_current_user_id), todo_service: TodoService = Depends(get_todo_service)):
    
    return await todo_service.insert_todos(request, writer_id=user_id)


# 할일 수정
@router.put("/{todo_id}", response_model=TodoSuccessResponse)
async def update_todo(todo_id: int, request: TodoUpdateRequest, user_id: int = Depends(get_current_user_id), todo_service: TodoService = Depends(get_todo_service)):
    return await todo_service.update_todo(request, todo_id, user_id)



# 할일 삭제
@router.delete("/{todo_id}", response_model=TodoSuccessResponse)
async def delete_todo(todo_id: int, user_id: int = Depends(get_current_user_id), todo_service: TodoService = Depends(get_todo_service)):
    return await todo_service.delete_todo(todo_id=todo_id, writer_id=user_id)
    



