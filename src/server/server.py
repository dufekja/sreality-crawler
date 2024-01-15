import hydra
import uvicorn
import psycopg2

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

CONF = {
    'host': 'db',
    'port': 5432,
    'database': 'srealitydb',
    'user': 'admin',
    'password': 'admin'
}

BODY = lambda body : f"""
        <html>
            <head><title>Crawled content</title></head>
            <body>{body}</body>
        </html>
    """

PROPERTY_ITEM = lambda title, img_url : f"""
        <div class='property'>
            <h2>{title}</h2>
            <img src="{img_url}">
        </div>
    """

@hydra.main(version_base=None, config_path='../../conf', config_name='config')
def main(config):
    CONF = config['db']
    uvicorn.run(app, host="0.0.0.0", port=8080)


@app.get("/", response_class=HTMLResponse)
async def root():

    # fetch data from database
    data = []
    try:
        conn = psycopg2.connect(**CONF)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM properties")
            data = cur.fetchall()

        conn.close()
    except Exception as err:
        return f"""{err}"""

    # append properties into body content
    body = ""
    for property in data:
        body += PROPERTY_ITEM(property[1], property[2])

    # return html content
    return BODY(body) if len(data) else BODY("No data")

if __name__ == "__main__":
    main()