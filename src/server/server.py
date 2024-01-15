import hydra

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.database.database import DatabaseSreality

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():

    data = []
    try:
        db = DatabaseSreality(conf={
            'database': 'srealitydb',
            'host': 'localhost',
            'port': 5432,
            'user': 'admin',
            'password': 'admin'
        })

        data = db.property_fetch_all()
        db.close()
    except Exception as err:
        return f"""{err}"""

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