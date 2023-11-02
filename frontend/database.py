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

    query = 'select * from cybervisionflows where '

    where_clauses = []
    if filter.source_ip is not None and filter.source_ip != '':
        where_clauses += [f"sourceip=\'{filter.source_ip}\'"]
    if filter.dest_ip is not None and filter.dest_ip != '':
        where_clauses += [f"destinationip=\'{filter.dest_ip}\'"]
    if filter.source_name is not None and filter.source_name != '':
        where_clauses += [f"source=\'{filter.source_name}\'"]
    if filter.dest_name is not None and filter.dest_name != '':
        where_clauses += [f"destination=\'{filter.dest_name}\'"]
    if filter.from_date is not None and filter.from_date != '':
        where_clauses += [f"lastseen>\'{filter.from_date.strftime('%Y/%m/%d, %H:%M:%S')}\'"]
    if filter.to_date is not None and filter.to_date != '':
        where_clauses += [f"lastseen<\'{filter.to_date.strftime('%Y/%m/%d, %H:%M:%S')}\'"]
    
    query += " and ".join(where_clauses)
    query += ';'

    print(query)

    cursor.execute(query)

    return [
        {
            'source': x[1],
            'sourceport': x[4],
            'direction': x[7],
            'dest': x[2],
            'destport': x[6],
            'protocol': x[12],
            'firstseen': x[8].strftime('%Y/%m/%d, %H:%M:%S'),
            'lastseen': x[9].strftime('%Y/%m/%d, %H:%M:%S'),
            'tags': x[13],
            'packets': x[10],
            'bytes': x[11],
            'dayssince': int(x[14]),
            'sourceip': x[3],
            'destip':x[5]
        } for x in cursor.fetchall()
    ]
