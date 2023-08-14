import asyncio
from datetime import date
import json
import pandas as pd
import os
import random
from module.crawler.article_crawler import ArticleCrawler
from module.extractor.data_preparation import NewsDuplicateProcessor, NewsTextRankProcessor


USER = '너의 로컬 주소를 입력'
file_path = f'{USER}/DailyGanzi-BE/module'

class NewsExtractor:
    def __init__(self):
        self.categories = ['정치', '경제', '사회', '생활문화', '세계', 'IT과학']
        self.categories_dict = ArticleCrawler().categories  # Assuming you have a dictionary mapping categories to IDs
        self.json_data = None
    def search_data(self):
        # Crawler articles
        crawler = ArticleCrawler()
        crawler.set_category(*self.categories)
        asyncio.run(crawler.start())  # Run crawler asynchronously
        return crawler.df_list

    def extract_data(self,df_list):
        # Load and preprocess data
        df = pd.concat(df_list)
        # Duplicate processing
        df = NewsDuplicateProcessor(df).preprocess_and_remove_duplicates()

        # TextRank keyword extraction
        textrank_processor = NewsTextRankProcessor(df)
        textrank_processor.start()

        self.top_keywords = textrank_processor.get_most_common_keywords()
        self.contents = textrank_processor.filter_data_with_keywords()

    def create_response_json(self):
        response_schema = {
            "updated": str(date.today()),
            "todayNews": {
                "hot_topic": [item[0] for item in self.top_keywords[:5]],
                "categories": []
            }
        }

        for category, keyword_dict in self.contents.items():
            category_info = {
                "category_name": category,
                "category_id": self.categories_dict[category],
                "details": {}
            }
            for keyword, df in keyword_dict.items():
                img_url_list = []  # List to hold unique image URLs for each keyword
                contents_list = []
                related_articles_list = []  # List to hold related articles
                for _, row in df.iterrows():
                    if row["img_url"] == "No Image":
                        continue
                    # if len(row["sentences"]) < 5:
                    #     continue
                    img_url_list.append(row["img_url"])
                    contents_list.extend(row["sentences"])

                    related_article = {
                        "press": row["company"],
                        "title": row["title"],
                        "preview": row["sentences"],
                        "url": row["articles_url"],
                    }
                    related_articles_list.append(related_article)

                    if len(contents_list) >= 3:
                        break

                if len(contents_list) >= 3:
                    selected_img_url = random.choice(img_url_list)
                    item = {
                        "contents": contents_list[:3],
                        "related": related_articles_list[:3]  # Add related articles
                    }
                    category_info["details"][keyword] = item
                    category_info["details"][keyword]["img_url"] = selected_img_url
            response_schema["todayNews"]["categories"].append(category_info)

        # Sort categories by ID
        sorted_category = sorted(response_schema["todayNews"]["categories"],
                                 key=lambda x: self.categories_dict.get(x["category_name"], ""))
        response_schema["todayNews"]["categories"] = sorted_category

        # (임시) JSON 데이터 저장 + version
        version = 0;
        while os.path.isfile(f'{file_path}/api_data_v' + str(version) + '.json'):
            version += 1
        with open(f'{file_path}/api_data_v' + str(version) + '.json', 'w', encoding='utf-8') as json_file:
            ilganzi_data = json.dumps(response_schema, indent=4, ensure_ascii=False)
            json_file.write(ilganzi_data)
        return ilganzi_data

    def start(self):
        self.extract_data(self.search_data())
        self.json_data = self.create_response_json()
        print('Done')
        return self.json_data

