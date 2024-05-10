import psycopg2
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

database = os.environ["PG_DATABASE"]
host = os.environ["PG_HOST"]
user = os.environ["PG_USERNAME"]
password = os.environ["PG_PASSWORD"]
port = os.environ["PG_PORT"]

conn = psycopg2.connect(database=database,
                        host=host,
                        user=user,
                        password=password,
                        port=port)

def put_flows(flows):
    cursor = conn.cursor()
    for flow in flows:
        try:
            cursor.execute(f"INSERT INTO cybervisionflows VALUES (\'{flow['id']}\', \
                        \'{flow['source']}\', \'{flow['dest']}\', \'{flow['sourceip']}\', \'{flow['sourceport']}\', \
                        \'{flow['destinationip']}\', \'{flow['destinationport']}\', \'{flow['direction']}\', \
                        \'{flow['firstseen']}\', \'{flow['lastseen']}\', \'{flow['packets']}\', \
                        \'{flow['bytes']}\', \'{flow['protocol']}\', \'{flow['tags']}\', \'{flow['dayssince']}\');")
            conn.commit()
        except:
            conn.commit()

def put_flow(flow):
    cursor = conn.cursor()

    try:
        cursor.execute(f"INSERT INTO cybervisionflows VALUES (\'{flow['id']}\', \
                        \'{flow['source']}\', \'{flow['dest']}\', \'{flow['sourceip']}\', \'{flow['sourceport']}\', \
                        \'{flow['destinationip']}\', \'{flow['destinationport']}\', \'{flow['direction']}\', \
                        \'{flow['firstseen']}\', \'{flow['lastseen']}\', \'{flow['packets']}\', \
                        \'{flow['bytes']}\', \'{flow['protocol']}\', \'{flow['tags']}\', \'{flow['dayssince']}\');")
        conn.commit()
    except:
        conn.commit()

def get_flows():
    cursor = conn.cursor()

    cursor.execute('select * from flows')

    return [
        {
            'id': x[0],
            'from_freq': x[1],
            'to_freq': x[2]
        } for x in cursor.fetchall()
    ]
