# DB 추상화 & 설정
# MongoDB 연동 & 컬렉션 정의
import json

from fastapi import requests
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["news"]


class MongoDB:
    def __init__(self, db_name="news"):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]


collections = {
    "related_news": db["related_news"],
    "title_contents": db["title_contents"],
    "title_keys": db["title_keys"],
    "news_details": db["news_details"],
    "news_categories": db["news_categories"],
    "news_data_list": db["news_data_list"],
    "today_news": db["today_news"],
}

# 초기데이터


async def insert_initial_data():
    cdn_link = "https://res.cloudinary.com/dedf7agck/raw/upload/v1692265642/api_data_v0_n4bnra.json"
    response = requests.get(cdn_link)

    if response.status_code == 200:
        content = response.content  # 바이트 데이터로 응답 받기
        decoded_content = content.decode('utf-8')  # UTF-8로 디코딩
        example_category = json.loads(decoded_content)  # JSON 파싱
        print(example_category)
    else:
        print("요청 실패:", response.status_code)

    collection = db.get_collection("today_news")
    await collection.insert_many(cdn_link)

