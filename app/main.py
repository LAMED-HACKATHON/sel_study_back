from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.users import router as user_router
from app.api.routes.todos import router as todo_router
from app.api.routes.plans import router as plan_router
from app.api.routes.feedback import router as feedback_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield  # The application runs during this context

app = FastAPI(
    title="FastAPI",
    description="FastAPI with MySQL async CRUD operations",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/api/users")
app.include_router(todo_router, prefix="/api/todos")
app.include_router(plan_router, prefix="/api/plans")
app.include_router(feedback_router, prefix="/api/feedback")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}
