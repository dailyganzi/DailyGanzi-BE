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
#
# data = dataloader()
# sample_file_path = FilePath("db/sample.json")

# 임시 저장된 json 가져오기
path = "C:/Users/charz/OneDrive/바탕 화면/lionhackerthon/DailyGanzi-BE/module"
with open(f'{path}/api_data_v0.json', "r",
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
        else:
            raise HTTPException(status_code=404, detail="Related news URL not found")
    raise HTTPException(status_code=404, detail="Category or keyword not found")

# detail 키워드별 정보 불러오기
@news_router.get("/api/{category_id}/newsPage/{keyword_id}")
async def get_category_keyword_news(category_id: int, keyword_id: int):
    # 주어진 데이터에서 카테고리와 키워드에 해당하는 정보 찾기
    category_data = example_category["todayNews"]["categories"]
    for category in category_data:
        if category["category_id"] == category_id:
            if 0 <= keyword_id < len(category["details"]):
                details = category["details"][keyword_id]
                keyword, content = list(details.items())[0]
                return {
                    "keyword": keyword,
                    "details": content["contents"]
                }
            else:
                raise HTTPException(status_code=404, detail="Related news URL not found")
    raise HTTPException(status_code=404, detail="Category or keyword not found")

# 관련 뉴스 정보 개별 불러오기
@news_router.get("/api/{category_id}/newsPage/{keyword_id}/related_news/{url_id}")
async def get_category_keyword_news(category_id: int, keyword_id: int, url_id : int):
    category_data = example_category["todayNews"]["categories"]
    for category in category_data:
        if category["category_id"] == category_id:
            if 0 <= keyword_id < len(category["details"]):
                details = category["details"][keyword_id]
                _, content = list(details.items())[0]
                related_news = content["related"]

                if 0 <= url_id < len(related_news):
                    return related_news[url_id]
                else:
                    raise HTTPException(status_code=404, detail="Related news URL not found")
    raise HTTPException(status_code=404, detail="Category or keyword not found")
