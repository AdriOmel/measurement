import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(host='dpg-cub96j3tq21c73ciajb0-a.frankfurt-postgres.render.com',
                            database='measurements_oz3i',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

def add_sensor(mac:str, sensor_type:str) -> list[dict]:
    sql = '''INSERT INTO Sensors(mac_adress, sensor_type) VALUES(%s, %s) RETURNING *;'''
    result = execute_query(sql, mac, sensor_type)
    return result
     
def check_sensor(mac:str, sensor_type:str) -> list[dict]:
    sql = '''SELECT * FROM Sensors WHERE (mac_adress=%s AND sensor_type=%s);'''
    result = execute_query(sql, mac, sensor_type)
    return result   

def add_measurements(sensor_id:int, sensor_value:float, correction:float) -> list[dict]:
    sql = '''INSERT INTO Measurments(sensor_id, sensor_value, correction) VALUES(%s, %s, %s) RETURNING *;'''
    result = execute_query(sql, sensor_id, sensor_value, correction)
    return result

def execute_query(sql:str, *args) -> list[dict]:
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql, args)
    rows = cur.fetchall()
    result = [dict(row) for row in rows]
    conn.commit()
    print(result)
    cur.close()
    conn.close() 
    return result