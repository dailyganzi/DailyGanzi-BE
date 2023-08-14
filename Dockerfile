FROM python:3.11

WORKDIR /

COPY requirements.txt .

RUN pip install --no-cache-dir  -r requirements.txt

RUN pip install uvicorn

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
