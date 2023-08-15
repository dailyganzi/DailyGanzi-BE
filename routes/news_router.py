from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import FilePath
from urllib.parse import unquote
from models.news_model import category_list, TodayNews, NewsDataList, NewsCategories, NewsDetails, TitleContents

news_router = APIRouter()


# 메인피드에서 카테고리 목록 조회
@news_router.get("/api/categories")
async def get_categories():
    return {"category_list": category_list}


@news_router.get("/api/{category_id}/newsPage")
async def get_category_news(category_id: int):
    example_category = NewsCategories.Config.json_schema_extra["example"]
    if example_category["category_id"] == category_id:
        return {
            "today_keys": example_category["title_keys"],
            "details": example_category["details"]
                }
    else:
        return {"message": "Category not found"}












