import psycopg2

DB_SCRIPT_PATH = "init.sql"

class DatabaseSreality:
    def __init__(self, conf):
        self.conn = psycopg2.connect(
            database = conf['database'],
            host = conf['host'],
            port = conf['port'],
            user = conf['user'],
            password = conf['password']
        )

    def property_insert(self, property):
        """ Insert property object into properties table """
        with self.conn.cursor() as cur:
            cur.execute(f"INSERT INTO properties (title, img_url) VALUES ('{property['title']}', '{property['img_url']}')")

    def property_fetch_all(self):
        """ Fetch all properties """

        data = []

        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM properties")
            data = cur.fetchall()

        return data


    def init_db(self):
        """ Run create.qsl script """
        with self.conn.cursor() as cur:
            with open(DB_SCRIPT_PATH, 'r') as f:
                cur.execute(f.read())
                self.commit()

    def commit(self):
        """ Commit changes """
        self.conn.commit()

    def close(self):
        """ Close connection """
        self.conn.close()