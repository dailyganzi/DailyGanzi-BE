from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.models.news import News
from bson import ObjectId


def get_collection_news(request: Request):
    return request.app.database["news"]


def create_news(request: Request, news_item: News = Body(...)):
    news_item = jsonable_encoder(news_item)
    new_news = get_collection_news(request).insert_one(news_item)
    created_news = get_collection_news(request).find_one({"_id": new_news.inserted_id})
    return created_news


def list_news(request: Request, limit: int):
    news_list = list(get_collection_news(request).find().limit(limit))
    return news_list


def find_news(request: Request, id: str):
    if news_item := get_collection_news(request).find_one({"_id": ObjectId(id)}):
        return news_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"News with id {id} not found!")


def delete_news(request: Request, id: str):
    deleted_news = get_collection_news(request).delete_one({"_id": ObjectId(id)})

    if deleted_news.deleted_count == 1:
        return f"News with id {id} deleted successfully"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"News with id {id} not found!")
