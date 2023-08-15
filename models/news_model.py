from typing import List, Dict
from pydantic import BaseModel, HttpUrl
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

with open('C:/Users/charz/OneDrive/바탕 화면/lionhackerthon/DailyGanzi-BE/module/api_data_v0.json', "r", encoding='utf-8') as file:
    data = json.load(file)
keys=list(data['todayNews']['categories'][0]['details'].keys())
print(data['todayNews']['categories'][0]['details'][keys[0]]['related'])

class RelatedNews(BaseModel):
    press: str
    title: str
    preview: str
    url: HttpUrl

    class Config:
        json_schema_extra = {
            "related": {
                "press": "세계일보" ,
                "title": "‘보수 원로’ 윤여준 尹에 “평소 실력 안 되는데 어떻게 잼버리 위기대응하겠나”" ,
                "preview": ["윤 전 장관은 ..."] ,
                "url": "https://n.news.naver.com/mnews/article/022/0003844477?sid=100"
            }
        }

class TitleContents(BaseModel):
    img_url: HttpUrl
    contents: List[str]
    related: List[RelatedNews]

    class Config:
        json_schema_extra = {
            "hungryNana": {
                "img_url": "https://picsum.photos/200/300",
                "contents": [
                    "나녕이가 배고파서 밥을 먹었다.",
                    "저녁밥 두 그릇이 없어짐.",
                    "나녕이가 배고파서 울었다."
                ],
                "related": [
                    RelatedNews.Config.json_schema_extra["related"]
                ],
            },
            "sleepyNana": {
                "img_url": "https://picsum.photos/200/300",
                "contents": [
                    "나녕이의 숙면시간은 0.5시간이다.",
                    "나녕이가 밤샘 작업을 했다.",
                    "속보 침대붕괴사건 발생"
                ],
                "related": [
                    RelatedNews.Config.json_schema_extra["related"]
                ],
            },
            "happyNana": {
                "img_url": "https://picsum.photos/200/300",
                "contents": [
                    "나녕이가 행복함을 느꼈다.",
                    "앵무새가 나녕이를 물었다.",
                    "나녕이가 맥북을 때렸다."
                ],
                "related": [
                    RelatedNews.Config.json_schema_extra["related"]
                ],
            }
        }


# 오늘의 키워드 리스트 모델
class TitleKeys(BaseModel):
    keys: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "keys": ["hungryNana", "sleepyNana", "happyNana"]
            }
        }


class NewsDetails(BaseModel):
    title1: dict[str, TitleContents]
    title2: dict[str, TitleContents]
    title3: dict[str, TitleContents]

    class Config:
        json_schema_extra = {
            "example": {
                "hungryNana": TitleContents.Config.json_schema_extra["hungryNana"],
                "sleepyNana": TitleContents.Config.json_schema_extra["sleepyNana"],
                "happyNana": TitleContents.Config.json_schema_extra["happyNana"]
            }

        }



class NewsCategories(BaseModel):
    category_name: str
    category_id: int
    title_keys: List[TitleKeys]
    details: NewsDetails


    class Config:
        json_schema_extra = {
            "example": {
                "category_name": "사회",
                "category_id": 102,
                "title_keys": TitleKeys.Config.json_schema_extra["example"]["keys"],
                "details": [
                    {
                        "hungryNana": NewsDetails.Config.json_schema_extra["example"]["hungryNana"],
                        "sleepyNana": NewsDetails.Config.json_schema_extra["example"]["sleepyNana"],
                        "happyNana": NewsDetails.Config.json_schema_extra["example"]["happyNana"]
                    }
                ]
            }
        }


class NewsDataList(BaseModel):
    hot_topic: List[str]
    categories: List[NewsCategories]

    class Config:
        json_schema_extra = {
            "example": {
                "hot_topic": ["나녕이", "침대붕괴사건", "앵무새"],
                "categories": [
                    NewsCategories.Config.json_schema_extra
                ]
            }
        }


class TodayNews(BaseModel):
    updated: str
    todayNews: NewsDataList

    class Config:
        json_schema_extra = {
            "example": {
                "updated": "2023-08-12",
                "todayNews": NewsDataList.Config.json_schema_extra["example"]
            }
        }


# 메인피드로 보낼 애들
category_name_list = ["IT과학", "경제", "사회", "생활문화", "세계", "정치"]
category_id_list = [105, 101, 102, 103, 104, 100]
category_list = {category_name: category_id
                 for category_name, category_id
                 in zip(category_name_list, category_id_list)}
