FROM python:3.12-slim

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

WORKDIR /opt
RUN echo "1"
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

COPY app .

CMD ["python3", "main.py"]