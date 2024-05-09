""" 
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

import requests, json, os, datetime
from dotenv import load_dotenv

#Read data from json file
def getJson(filepath):
	with open(filepath, 'r') as f:
		json_content = json.loads(f.read())
		f.close()

	return json_content

#Write data to json file
def writeJson(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)
    f.close()

def get_days_since(unixtime):
    then = datetime.datetime.fromtimestamp(unixtime)
    now = datetime.datetime.now()
    diff = now-then
    return diff.days

def get_components():
    host = os.environ['CYBERVISION_HOST']
    token = os.environ['CYBERVISION_TOKEN']
    url = f"https://{host}/api/3.0/components"
    headers = {
        "Accept" : "application/json",
         "x-token-id" : token
    }
    components = requests.get(url, headers=headers, verify=False).json()
    writeJson('components.json', components)

def get_ip_for_component(name):
    components = getJson('components.json')
    for c in components:
        if c['label'] == name:
            return c['ip']
    return '255.255.255.255'

def get_flows_since_yesterday():
    get_components()

    host = os.environ['CYBERVISION_HOST']
    token = os.environ['CYBERVISION_TOKEN']

    to_date = f"{datetime.datetime.now().strftime('%s')}000"
    from_date = f"{(datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%s')}000"

    url = f"https://{host}/api/3.0/flows?from={from_date}&to={to_date}"

    headers = {
        "Accept" : "application/json",
        "x-token-id" : token
    }

    flows = requests.get(url, headers=headers, verify=False).json()

    print(f"BACKEND: Found {len(flows)} flows")

    db_formatted_flows = []
    for f in flows:
        tag_list = []
        for t in f['tags']:
            tag_list += [t['label']]
        db_formatted_flows += [
            {
                "id" : f["id"],
                "source" : f['left']['label'],
                "dest" : f['right']['label'],
                "sourceport" : f['srcPort'],
                "destinationport" : f['dstPort'],
                "destinationip" : get_ip_for_component(f['right']['label']),
                "sourceip" : get_ip_for_component(f['left']['label']),
                "direction" : f['direction'],
                "firstseen" : datetime.datetime.fromtimestamp(f['firstActivity']/1000).strftime('%Y/%m/%d, %H:%M:%S'),
                "lastseen" : datetime.datetime.fromtimestamp(f['lastActivity']/1000).strftime('%Y/%m/%d, %H:%M:%S'),
                "packets" : f['packetsCount'],
                "bytes" : f['bytesCount'],
                "protocol" : f['protocol'],
                "tags" : ', '.join(tag_list),
                "dayssince" : get_days_since(f['lastActivity']/1000)
            }
        ]

    print(len(db_formatted_flows))

    writeJson('flows.json', db_formatted_flows)

    return db_formatted_flows