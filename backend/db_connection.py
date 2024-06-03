import psycopg2
from flask import g

# TimescaleDB 접속 정보
db_host = "qi2xwq7bbz.hab5fz9qvo.tsdb.cloud.timescale.com"
db_port = 36757
db_name = "tsdb"
db_user = "tsdbadmin"
db_password = "2024bkms1team8"
timescale = True
def get_db_connection():
    if 'conn' not in g:
        # TimescaleDB
        if timescale:
            g.conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=db_password,
                sslmode='require'
            )
        # Local
        else:
            g.conn = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="postgres",
                password="postgres",
                port="5555"
            )
        print("Database connection successful")
    return g.conn



def close_db_connection():
    conn = g.pop('conn', None)
    if conn is not None:
        conn.close()
        print("Database connection closed")


