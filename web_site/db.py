import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(host=os.environ['DB_HOST'],
                            database=os.environ['DB_DATABASE'],
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

def add_measurements(sensor_id:int, sensor_value:float) -> dict:
    sql = '''INSERT INTO Measurments(sensor_id, sensor_value) VALUES(%s, %s, %s) RETURNING *;'''
    result = execute_query(sql, sensor_id, sensor_value)
    return result[0]

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

def get_measurements(sensor_type:str, mac_address:str) -> list[dict]:
    sql = '''SELECT sensor_value+correction as sensor_value, datetime FROM measurments JOIN sensors ON (sensors.id=sensor_id) WHERE sensor_type=%s AND mac_adress=%s;'''
    result = execute_query(sql, sensor_type, mac_address)
    return result

def update_sensor(correction:float, sensor_location:str, units:str, id:int) -> dict:
    sql = '''UPDATE sensors SET correction=%s, sensor_location=%s, units=%s WHERE id=%s RETURNING *;'''
    result = execute_query(sql, correction, sensor_location, units, id)
    return result[0]