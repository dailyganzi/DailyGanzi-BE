from fastapi import APIRouter
from models.news_model import category_list, NewsCategories

news_router = APIRouter()


# 메인피드에서 카테고리 목록 조회
@news_router.get("/api/categories")
async def get_categories():
    return {"category_list": category_list}


# sample_file_path = FilePath("db/sample.json")
#
# with open(sample_file_path, "r") as file:
#     sample_file_content = json.load(file)


# 카테고리 선택 -> 해당 카테고리 상세페이지 조회 (일단 Config를 넣어놨음)
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


# 오전 12시 이후 뉴스 업데이트











