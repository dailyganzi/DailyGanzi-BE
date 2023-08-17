import os
import json
from fastapi import FastAPI

app = FastAPI()

# 파일 경로 설정
file_path = os.path.join(os.path.dirname(__file__), "/api_data_v0.json")


# 파일 읽기
def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

