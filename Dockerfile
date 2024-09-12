FROM python:3

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir scrapy

RUN apt-get update && \
    apt-get upgrade && \
    apt-get install sqlite3

WORKDIR /app

CMD ["bash"]