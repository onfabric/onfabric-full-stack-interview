from fastapi import APIRouter

from app.api.routes import health, user

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])

user_router = APIRouter()
user_router.include_router(user.router, tags=["users"])