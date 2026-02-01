from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield  # The application runs during this context

app = FastAPI(
    title="AGENT CHAT API",
    description="FastAPI with MySQL async CRUD operations",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router, prefix="")


@app.get("/")
async def root():
    return {"message": "AGENT CHAT API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}
