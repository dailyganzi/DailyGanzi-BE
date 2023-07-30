from fastapi import APIRouter
from src.endpoints import news, users

router = APIRouter()

router.include_router(news.router)
router.include_router(users.router)