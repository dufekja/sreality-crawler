# Real estate scraper

Aim of this project is to scrape items from `sreality.cz` and show them on a simple page.

## Steps
- use scrapy framework to get first 500 items from sreality.cz (title, image url), (flats, sell)
- save scraped data into Postgresql db
- implement siple HTTP python server (I'll use fastapi) and show scraped data on a simple page (title, image)
- create docker compose config -> localhost:8080 

## Result:

I was not able to get working container for crawler and docker compose. But locally the code works with these commands:

Deps:
```
    python -m pip install --upgrade -r requirements.txt
```

Database:
```
    docker build -f dockerfiles/db.dockerfile -t postgresql .
    docker run -d --name db -p 5432:5432 postgresql
```

Crawler:
```
    python src/crawler/crawler.py
```

Server:
```
    uvicorn src.server.server:app --port 8080
```