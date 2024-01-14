import hydra
import database

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():

    db = database.DatabaseSreality(conf={
        'database': 'sreality',
        'host': 'localhost',
        'port': 5432,
        'user': 'admin',
        'password': 'admin'
    })

    data = db.property_fetch_all()

    property_html = lambda title, img_url : f"""
        <div class='property'>
            <h2>{title}</h2>
            <img src="{img_url}">
        </div>
    """

    # append properties into body content
    body = ""
    for property in data:
        body += property_html(property[1], property[2])

    return f"""
    <html>
        <head><title>Crawled content</title></head>
        <body>{body}</body>
    </html>
    """