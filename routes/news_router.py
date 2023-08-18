import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import FilePath
from urllib.parse import unquote
from models.news_model import category_list, TodayNews, NewsDataList, NewsCategories, NewsDetails, TitleContents
from module.dataloader import NewsExtractor
from db.database import collections
import json
import requests
import uvicorn
import asyncio

news_router = APIRouter()

# # 데이터 불러오는 함수
# ROOT = '/Users/nyungnim/Documents'
# path = f'{ROOT}/DailyGanzi-BE'

# @news_router.get("/update_data")
# async def update_data():
#     ROOT = '/Users/nyungnim/Documents'
#     path = f'{ROOT}/DailyGanzi-BE'
#     data = await dataloader(path, 100)  # await 추가
#
#
# async def dataloader(path, pages):
#     # 임시 데이터 저장하기 위해 path 입력 해주고 실행시켜야함!
#     # 백엔드 완성되면 삭제할 예정
#     news_extractor = NewsExtractor(path,pages)
#     await news_extractor.start()
#     return news_extractor.json_data


# data = dataloader(path,100)
#
# await data

# sample_file_path = FilePath("db/sample.json")
# 임시 저장된 json 가져오기
# path = "https://res.cloudinary.com/dedf7agck/raw/upload/v1692179424/api_data_v0_q2v9fy.json"
# with open(path, "r",
#           encoding='utf-8') as file:
#     example_category = json.load(file)
# news_router = APIRouter()

# cdn_link = "https://res.cloudinary.com/dedf7agck/raw/upload/v1692265642/api_data_v0_n4bnra.json"
# response = requests.get(cdn_link)

# if response.status_code == 200:
#     content = response.content  # 바이트 데이터로 응답 받기
#     decoded_content = content.decode('utf-8')  # UTF-8로 디코딩
#     example_category = json.loads(decoded_content)  # JSON 파싱
#     print(example_category)
# else:
#     print("요청 실패:", response.status_code)

# POST
# CRUD (create & update & Delete) - 초기 데이터 추가 이후 매일 오전 12시에 업데이트 됨
# 매일 오전 12시에 실행되는 함수
async def update_news_data():
    ROOT = '/Users/nyungnim/Documents'
    path = f'{ROOT}/DailyGanzi-BE'

    for _ in range(3):  # 3일치 데이터를 생성하고 저장
        news_extractor = NewsExtractor(path, pages=100)
        news_data = await news_extractor.start()

        # 오늘의 날짜를 기준으로 날짜를 계산합니다.
        today = datetime.today().date()
        delta = datetime.timedelta(days=1)
        current_date = today - delta * _

        # 오늘의 뉴스 데이터를 컬렉션에 저장
        today_news_collection = collections["today_news"]
        today_news_collection.insert_one({
            "updated": str(current_date),
            "todayNews": news_data["todayNews"]
        })

        print(f"Data for {current_date} added to today_news collection")

        # 가장 오래된 데이터 삭제
        oldest_date = today - delta * 3
        today_news_collection.delete_one({"updated": str(oldest_date)})

        print(f"Data for {oldest_date} deleted from today_news collection")

# asyncio 이벤트 루프를 실행하여 함수를 매일 오전 12시에 실행
async def main():
    while True:
        current_time = datetime.now()
        target_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

        # 계산된 대상 시간까지 대기 후 데이터 업데이트 실행
        await asyncio.sleep((target_time - current_time).total_seconds())
        await update_news_data()

if __name__ == "__main__":
    asyncio.run(main())

# GET

# # 메인피드에서 카테고리 목록 조회
# @news_router.get("/api/hot-topic")
# async def get_topics():
#     hot_topic = example_category["todayNews"]["hot_topic"]
#     return {"hot_topic": hot_topic[:3]}
@news_router.get("/api/hot-topic")
async def get_topics():


# @news_router.get("/api/categories")
# async def get_categories():
#     category_dict = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105}
#     return {"categories": category_dict}

# # 상세페이지 - 키워드별 정보 불러오기
# @news_router.get("/api/{category_id}/newsPage")
# async def get_category_keyword_news(category_id: int):
#     # 주어진 데이터에서 카테고리와 키워드에 해당하는 정보 찾기
#     category_data = example_category["todayNews"]["categories"]
#     for category in category_data:
#         if category["category_id"] == category_id:
#             # 키워드를 추출하여 리스트에 저장
#             keywords = [detail["keyword"] for detail in category["details"]]
#             return {
#                 "category" : category["category_name"],
#                 "today_topic" :  keywords,
#                 "details": category['details'],
#             }

#     # 카테고리 아이디에 해당하는 정보가 없는 경우 오류 발생
#     raise HTTPException(status_code=404, detail="Category not found")




# 빈통 3개 만들어서 안에서 데이터 들락날락 초기 데이터 -> 빈 박스 3개 -> 들락날락