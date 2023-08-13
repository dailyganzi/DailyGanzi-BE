from typing import List, Dict
from pydantic import BaseModel, HttpUrl


class TitleContents(BaseModel):
    img_url: HttpUrl
    contents: List[str]
    articles_url: List[HttpUrl]
    keywords: List[str]

    class Config:
        schema_extra = {
            "hungryNana": {
                "img_url": "https://picsum.photos/200/300",
                "contents": ["나녕이가 배고파서 밥을 먹었다.", "저녁밥 두 그릇이 없어짐.", "나녕이가 배고파서 울었다."],
                "articles_url": ["https://example.com/article1", "https://example.com/article2",
                                 "https://example.com/article3"],
                "keywords": ["나녕이", "저녁밥", "울었다"]
            },
            "sleepyNana": {
                "img_url": "https://picsum.photos/200/300",
                "contents": ["나녕이의 숙면시간은 0.5시간이다.", "나녕이가 밤샘 작업을 했다.", "속보 침대붕괴사건 발생"],
                "articles_url": ["https://example.com/article1", "https://example.com/article2",
                                 "https://example.com/article3"],
                "keywords": ["밤샘", "숙면시간", "침대붕괴사건"]
            },
            "happyNana": {
                "img_url": "https://picsum.photos/200/300",
                "contents": ["나녕이가 행복함을 느꼈다.", "앵무새가 나녕이를 물었다.", "나녕이가 맥북을 때렸다."],
                "articles_url": ["https://example.com/article1", "https://example.com/article2",
                                 "https://example.com/article3"],
                "keywords": ["행복함", "앵무새", "맥북"]
            }
        }


class NewsDetails(BaseModel):
    title1: TitleContents
    title2: TitleContents
    title3: TitleContents

    class Config:
        schema_extra = {
            "example": {
                "title1": TitleContents.Config.schema_extra["hungryNana"],
                "title2": TitleContents.Config.schema_extra["sleepyNana"],
                "title3": TitleContents.Config.schema_extra["happyNana"]
            }
        }


class NewsCategories(BaseModel):
    category_name: str
    category_id: int
    details: List[NewsDetails]

    class Config:
        schema_extra = {
            "example": {
                "category_name": "사회",
                "category_id": 102,
                "details": [
                    NewsDetails.Config.schema_extra["example"]["title1"],
                    NewsDetails.Config.schema_extra["example"]["title2"],
                    NewsDetails.Config.schema_extra["example"]["title3"]
                ]
            }
        }


class NewsDataList(BaseModel):
    hot_topic: List[str]
    categories: List[NewsCategories]

    class Config:
        schema_extra = {
            "example": {
                "hot_topic": ["나녕이", "침대붕괴사건", "앵무새"],
                "categories": [
                    NewsCategories.Config.schema_extra
                ]
            }
        }


class TodayNews(BaseModel):
    updated: str
    todayNews: NewsDataList

    class Config:
        schema_extra = {
            "example": {
                "updated": "2023-08-12",
                "todayNews": NewsDataList.Config.schema_extra["example"]
            }
        }


# 메인피드로 보낼 애들
category_name_list = ["IT과학", "경제", "사회", "생활문화", "세계", "정치"]
category_id_list = [105, 101, 102, 103, 104, 100]
category_list = {category_name: category_id
                 for category_name, category_id
                 in zip(category_name_list, category_id_list)}
