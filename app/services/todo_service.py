from datetime import datetime, time

from app.model.todos import Todo
from app.repositories.todo_repo import TodoRepository
from app.schemas.todos import TodoInsertReqeust, TodoResponse, TodoSuccessResponse, TodosRequest, TodoUpdateRequest


class TodoService:

        def __init__(self, todo_repo: TodoRepository) -> None:
            self.todo_repo = todo_repo

        async def get_today_todos(self, request: TodosRequest) -> list[TodoResponse]:
        
            todos = await self.todo_repo.get_today_todos_by_user_id(request.user_id, request.target_date)

            result = []
            for todo_id, writer_id, title, content, status_yn, subject_name, todo_type, img_url1, img_url2, file_url1, file_url2, created_at in todos:
                result.append(
                    TodoResponse(
                        todo_id=todo_id,
                        writer_id=writer_id,
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


        async def insert_todos(self, request: TodoInsertReqeust, writer_id: int) -> TodoSuccessResponse:

            dates = sorted(request.target_date)

            insert_datas: list[Todo] = []

            if request.routine_yn == 1:
                for date in dates:
                    insert_datas.append(
                        Todo(
                            user_id=request.user_id,
                            writer_id=writer_id,
                            subject_id=request.subject_id,
                            todo_type="routine",
                            title=request.title,
                            content=request.content,
                            file_url1=request.file_url1,
                            file_url2=request.file_url2,
                            created_at=datetime.combine(date, time.min),
                            end_time=date,
                        )
                    )
            else:
                end_date = dates[-1]
                insert_datas.append(
                    Todo(
                        user_id=request.user_id,
                        writer_id=writer_id,
                        subject_id=request.subject_id,
                        todo_type="homework",
                        title=request.title,
                        content=request.content,
                        file_url1=request.file_url1,
                        file_url2=request.file_url2,
                        end_time=end_date,
                    )
                )

            await self.todo_repo.insert_todos(insert_datas)

            return TodoSuccessResponse(success=True)

        async def update_todo(self, request: TodoUpdateRequest, todo_id: int, writer_id: int) -> TodoSuccessResponse:
            
            items = request.model_dump(exclude_unset=True)

            await self.todo_repo.update_todo(todo_id=todo_id, writer_id=writer_id, items=items)
            return TodoSuccessResponse(success=True)

        async def delete_todo(self, todo_id: int, writer_id: int):

            await self.todo_repo.delete_todo(todo_id=todo_id, writer_id=writer_id)
            return TodoSuccessResponse(success=True)
            