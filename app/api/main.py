from fastapi import APIRouter

from .routes import expenses, login, reports, users

api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(expenses.router)
api_router.include_router(reports.router)
