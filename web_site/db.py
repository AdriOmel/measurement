import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(host='dpg-cub96j3tq21c73ciajb0-a.frankfurt-postgres.render.com',
                            database='measurements_oz3i',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
    '''CREATE TABLE measurments (
        temperature     float4,
        humidity        int,
        datetime        timestamptz
    );''')
    conn.commit()
    cur.close()
    conn.close() 

def print_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
    '''SELECT * FROM pg_catalog.pg_tables WHERE tablename LIKE '%measurments%';''')
    result = cur.fetchall()
    print(result)
    cur.close()
    conn.close() 

create_table()
print_table()