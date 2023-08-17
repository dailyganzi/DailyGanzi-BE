# DB 추상화 & 설정
# MongoDB 연동 & 컬렉션 정의

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


class MongoDB:
    def init(self, db_name="news"):
        self.client = AsyncIOMotorClient(MONGO_URI)
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]


client = MongoClient(MONGO_URI)
db = client["news"]

related_news_collection = db["related_news"]
title_contents_collection = db["title_contents"]
title_keys_collection = db["title_keys"]
news_details_collection = db["news_details"]
news_categories_collection = db["news_categories"]
news_data_list_collection = db["news_data_list"]
today_news_collection = db["today_news"]