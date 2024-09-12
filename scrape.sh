rm balsas.db
sqlite3 balsas.db < init.sql
scrapy crawl politicians
scrapy crawl answers