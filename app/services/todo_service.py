from app.repositories.todo_repo import TodoRepository
from app.schemas.todos import TodoResponse, TodosRequest


class TodoService:

        def __init__(self, todo_repo: TodoRepository) -> None:
            self.todo_repo = todo_repo

        async def get_today_todos(self, request: TodosRequest) -> list[TodoResponse]:
        
            todos = await self.todo_repo.get_today_todos_by_user_id(request.user_id, request.target_date)

            result = []
            for todo_id, title, content, status_yn, subject_name, todo_type, img_url1, img_url2, file_url1, file_url2, created_at in todos:
                result.append(
                    TodoResponse(
                        todo_id=todo_id,
                        title = title,
                        content = content,
                        status_yn=status_yn,
                        subject_name = subject_name,
                        todo_type=todo_type,
                        img_url1=img_url1,
                        img_url2=img_url2,
                        file_url1=file_url1,
                        file_url2=file_url2,
                        created_at=created_at
                    )
                )
            return result


        async def get_today_todo(self, todo_id: int) -> TodoResponse:
            return await self.todo_repo.get_today_todo_by_todo_id(todo_id)
            