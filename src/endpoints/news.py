from fastapi import APIRouter, Body, Request, status
from typing import List
from src.models.news import News

import src.rules.news as news


router = APIRouter(prefix="/news", tags=["News"])


@router.post("/", response_description="Create a new news", status_code=status.HTTP_201_CREATED, response_model=News)
def create_news(request: Request, news_item: News = Body(...)):
    return news.create_news(request, news_item)


@router.get("/", response_description="List news", response_model=List[News])
def list_news(request: Request):
    return news.list_news(request, 100)


@router.get("/{id}", response_description="Get a single news by id", response_model=News)
def find_news(request: Request, id: str):
    return news.find_news(request, id)


@router.delete("/{id}", response_description="Delete a news")
def delete_news(request: Request, id: str):
    return news.delete_news(request, id)
