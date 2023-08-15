from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import FilePath
from urllib.parse import unquote
from models.news_model import category_list, TodayNews, NewsDataList, NewsCategories, NewsDetails, TitleContents
from module.dataloader import NewsExtractor
import json

# 데이터 불러오는 함수
# def dataloader():
#     # 임시 데이터 저장하기 위해 path 입력 해주고 실행시켜야함!
#     # 백엔드 완성되면 삭제할 예정
#     news_extractor = NewsExtractor()
#     news_extractor.start()
#     return news_extractor.json_data
# data = dataloader()
# sample_file_path = FilePath("db/sample.json")

# 임시 저장된 json 가져오기
with open('{your_path}/api_data_v0.json', "r",
          encoding='utf-8') as file:
    example_category = json.load(file)

news_router = APIRouter()


# 메인피드에서 카테고리 목록 조회
@news_router.get("/api/categories")
async def get_categories():
    category_list = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105}
    return {"category_list": category_list}

@news_router.get("/api/{category_id}/newsPage")
async def get_category_news(category_id: int):
    category_data = example_category["todayNews"]["categories"]
    for category in category_data:
        if category["category_id"] == category_id:
            return {
                "category_name": category["category_name"],
                "details": category["details"]
            }

    return {"message": "Category not found"}







