from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes.users import router as user_router
from app.api.routes.todos import router as todo_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield  # The application runs during this context

app = FastAPI(
    title="FastAPI",
    description="FastAPI with MySQL async CRUD operations",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(user_router, prefix="/api/users")
app.include_router(todo_router, prefix="/api/todos")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}
