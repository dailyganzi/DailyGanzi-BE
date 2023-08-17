# DB 추상화 & 설정
# MongoDB 연동 & 컬렉션 정의

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
