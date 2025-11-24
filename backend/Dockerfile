FROM python:3.12

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

RUN pip install fastapi uvicorn sqlalchemy

COPY . .

CMD ["fastapi", "run", "app/main.py"]