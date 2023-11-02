import psycopg2
import os
from dotenv import load_dotenv

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
        cursor.execute(f"INSERT INTO cybervisionflows VALUES (\'{flow['id']}\', \
                       \'{flow['source']}\', \'{flow['dest']}\', \'{flow['sourceip']}\', \'{flow['sourceport']}\', \
                       \'{flow['destinationip']}\', \'{flow['destinationport']}\', \'{flow['direction']}\', \
                       \'{flow['firstseen']}\', \'{flow['lastseen']}\', \'{flow['packets']}\', \
                       \'{flow['bytes']}\', \'{flow['protocol']}\', \'{flow['tags']}\', \'{flow['dayssince']}\');")

def get_flows(filter):
    cursor = conn.cursor()

    query = 'select * from cybervisionflows'

    where_clauses = []
    if filter.source_ip is not None and filter.source_ip != '':
        where_clauses += [f"where sourceip=\'{filter.source_ip}\'"]
    if filter.dest_ip is not None and filter.dest_ip != '':
        where_clauses += [f"where destinationip=\'{filter.dest_ip}\'"]
    if filter.source_name is not None and filter.source_name != '':
        where_clauses += [f"where source=\'{filter.source_name}\'"]
    if filter.dest_name is not None and filter.dest_name != '':
        where_clauses += [f"where destination=\'{filter.dest_name}\'"]
    


    cursor.execute('select * from flows')

    return [
        {
            'id': x[0],
            'from_freq': x[1],
            'to_freq': x[2]
        } for x in cursor.fetchall()
    ]
