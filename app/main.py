from fastapi import FastAPI

from app.core.config import settings

from .api.main import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="An API for managing expenses the right way.",
)

app.include_router(api_router, prefix=settings.API_V1_STR)
