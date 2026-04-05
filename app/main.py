from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.session import SessionLocal
from app.db.init_db import init_first_superuser, create_tables
from app.api.v1.api import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    
    async with SessionLocal() as db:
        await init_first_superuser(db)
    
    yield

app = FastAPI(
    title="BlogFastAPI",
    description="Blog API with FastAPI & PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    return {"status": "ok"}