from typing import List, Dict
from pydantic import BaseModel, HttpUrl, Field
from bson import ObjectId


class NewsDetail(BaseModel):
    img_url: HttpUrl
    content: List[str]
    articles_url: List[HttpUrl]


class CategoryDetail(BaseModel):
    title1: List[NewsDetail]
    title2: List[NewsDetail]
    title3: List[NewsDetail]


class NewsArticle(BaseModel):
    _id: ObjectId = Field(..., alias="_id")
    updated: str
    category_name: str
    category_id: int
    details: List[CategoryDetail]

