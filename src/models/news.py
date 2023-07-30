from pydantic import BaseModel, Field, HttpUrl
from typing import List


class News(BaseModel):
    title: str
    category_id: int
    summary: str
    related_img: List[HttpUrl]
    related_articles: List[HttpUrl]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "title": "Happy Nana",
                "category_id": 102,
                "summary": "Uzzurago Mulba jinjja ddaerinda",
                "related_img": [
                    "https://example.com/image1.jpg",
                    "https://example.com/image2.jpg"
                ],
                "related_articles": [
                    "https://example.com/article/1",
                    "https://example.com/article/2"
                ]
            }
        }