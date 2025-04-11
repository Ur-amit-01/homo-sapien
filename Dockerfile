FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt update && apt install -y git
RUN pip install --no-cache-dir -r requirements.txt

CMD gunicorn app:app & python3 main.py
