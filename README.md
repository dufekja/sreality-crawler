# Real estate scraper

Aim of this project is to scrape items from `sreality.cz` and show them on a simple page.

## Steps
- use scrapy framework to get first 500 items from sreality.cz (title, image url), (flats, sell)
- save scraped data into Postgresql db
- implement siple HTTP python server (I'll use fastapi) and show scraped data on a simple page (title, image)
- create docker compose config -> localhost:8080 

## How to run:

On ubuntu run: ``` docker compose up --build ```
- make sure, you don't have occupied ports 8080 and 5432 by different services

