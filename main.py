from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from routes.news_router import news_router
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
app = FastAPI()

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

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
