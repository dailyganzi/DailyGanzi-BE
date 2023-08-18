import asyncio

import schedule
from fastapi import FastAPI
from pymongo import MongoClient
from starlette.middleware.base import BaseHTTPMiddleware

from module.data_update import run_scheduler, update_news_data
from routes.news_router import news_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
app = FastAPI()

# MongoDB 연결 설정
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
today_news_collection = db['todayNews']

# 테스트용
@app.get("/")
async def main() -> dict:
    return {
        "message": "DailyGanzi Main Feed"
    }

# 뉴스 관련 라우터
app.include_router(news_router)
# CORS 설정
origins = [
    # "http://localhost:5500/",
    # "https://dailyganzi.github.io/Dailyganzi-FE/",
    # "http://127.0.0.1:5500/"
    "*"
]

# MiddleWare
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # 이건 혹시 몰라서 넣어둔 거
    allow_methods=["*"],
    allow_headers=["*"],
)

class CustomMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self,request,call_next):
        response = await call_next(request)
        return response

app.add_middleware(CustomMiddleWare)


# 스케줄링 함수
async def schedule_task():
    while True:
        await asyncio.sleep(1)  # 이벤트 루프가 차단되지 않도록 일시적으로 잠시 대기
        schedule.run_pending()

# 비동기 이벤트 루프 실행
async def start_background_tasks():
    asyncio.create_task(schedule_task())
    asyncio.create_task(update_news_data())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    scheduled_time = "00:30"
    # 스케줄링 함수 등록
    schedule.every().day.at(scheduled_time).do(lambda: asyncio.create_task(update_news_data()))
    # 비동기 이벤트 루프 실행
    loop.run_until_complete(start_background_tasks())
    uvicorn.run(app, port=8000)