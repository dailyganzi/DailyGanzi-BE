from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
import datetime

# MongoDB 연결 설정
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
today_news_collection = db['todayNews']

def load_today_data_from_db():
    # 오늘 날짜 계산
    today = datetime.datetime.today().date()
    today_data = today_news_collection.find_one({"updated": str(today)})
    return today_data

example_category = load_today_data_from_db()

news_router = APIRouter()

# 메인피드에서 카테고리 목록 조회
@news_router.get("/api/hot-topic")
async def get_topics():
    hot_topic = example_category["todayNews"]["hot_topic"]
    return {"hot_topic": hot_topic[:3]}


@news_router.get("/api/categories")
async def get_categories():
    category_dict = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105}
    return {"categories": category_dict}


# 상세페이지 - 키워드별 정보 불러오기
@news_router.get("/api/{category_id}/newsPage")
async def get_category_keyword_news(category_id: int):
    # 주어진 데이터에서 카테고리와 키워드에 해당하는 정보 찾기
    category_data = example_category["todayNews"]["categories"]
    for category in category_data:
        if category["category_id"] == category_id:
            # 키워드를 추출하여 리스트에 저장
            keywords = [detail["keyword"] for detail in category["details"]]
            return {
                "category" : category["category_name"],
                "today_topic" :  keywords,
                "details": category['details'],
            }

    # 카테고리 아이디에 해당하는 정보가 없는 경우 오류 발생
    raise HTTPException(status_code=404, detail="Category not found")