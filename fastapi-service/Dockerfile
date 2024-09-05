FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /api
COPY requirements.txt requirements.txt
RUN  pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . /api

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]