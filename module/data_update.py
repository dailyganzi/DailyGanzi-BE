import asyncio
import schedule
import time
import datetime
from pymongo import MongoClient
from module.dataloader import NewsExtractor
import json

async def update_news_data():
    ROOT = 'C:/Users/charz/OneDrive/바탕 화면/lionhackerthon/'
    path = f'{ROOT}/DailyGanzi-BE'

    news_extractor = NewsExtractor(path, 100)
    await news_extractor.start()

    # MongoDB 연결 설정
    client = MongoClient('mongodb://localhost:27017/')
    db = client['mydatabase']
    today_news_collection = db['todayNews']

    news_entry = json.loads(news_extractor.json_data)
    # 오늘의 날짜 계산
    today = datetime.datetime.today().date()

    # 오늘의 뉴스 데이터를 컬렉션에 저장
    today_news_collection.insert_one(news_entry)

    print(f"Data for {today} added to today_news collection")
    client.close()  # 연결 종료

def run_scheduler():
    # 무한 루프로 스케줄링 작업 수행
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    scheduled_time = "20:50"

    # 스케줄링 함수 등록
    schedule.every().day.at(scheduled_time).do(lambda: loop.run_until_complete(update_news_data()))
    # 비동기 이벤트 루프 실행
    run_scheduler()