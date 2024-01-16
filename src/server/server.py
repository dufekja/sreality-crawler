import hydra
import uvicorn
import psycopg2


from sources import BODY, PROPERTY_ITEM

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@hydra.main(version_base=None, config_path='../../conf', config_name='config')
def main(config):
    global CONF
    CONF = config['db']['db']
    
    uvicorn.run(app, host="0.0.0.0", port=8080)
    

def db_connect():
    """ Connect to database and return connection object """
    return psycopg2.connect(
        host = 'db',
        port = 5432,
        database = CONF['database'],
        user = CONF['user'],
        password = CONF['password']
    )

@app.get("/", response_class=HTMLResponse)
async def root():

    # fetch data from database
    data = []

    try:
        conn = db_connect()
        
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