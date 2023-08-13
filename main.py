from fastapi import FastAPI
from routes.news_router import news_router
from routes.users_router import users_router

app = FastAPI()


# 테스트용
@app.get("/")
async def main() -> dict:
    return {
        "message": "DailyGanzi Main Feed"
    }

# 뉴스 관련 라우터
app.include_router(news_router)
# 유저 관련 라우터
app.include_router(users_router)

