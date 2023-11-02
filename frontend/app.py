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

# Import Section
from flask import Flask, render_template, request, url_for, redirect
from collections import defaultdict
import datetime, math
import requests
import json, csv
from dotenv import load_dotenv
import os
import cybervision
from flask import send_file as flask_send_file
#import merakiAPI
from dnacentersdk import api
import database

# load all environment variables
load_dotenv()

# Global variables
app = Flask(__name__)
FILTER = cybervision.Filter()
FLOWS_PER_PAGE = 15

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


##Routes
#Instructions

#Index
@app.route('/', methods=["GET", "POST"])
def index():
    global FILTER
    if request.method == "POST":
        filter = cybervision.Filter(
            source_name=request.form.get("source-name"),
            dest_name=request.form.get("dest-name"),
            source_ip=request.form.get("source-ip"),
            dest_ip=request.form.get("dest-ip"),
            from_date=request.form.get("from-date"),
            to_date=request.form.get("to-date")
        )

        deadline = 0   

        FILTER = filter
        print(f"Filter submitted: {filter.to_json()}")

        # Get flows
        flows = database.get_flows(filter)
        writeJson('flows.json', flows)

        return redirect(f"/flows?page=0&deadline={deadline}")

    try:
        #Page without error message and defined header links 
        writeJson('components.json', cybervision.get_components())
        return render_template('home.html', filter=cybervision.Filter().to_json(), flows=[], deadline=0, label_list=getJson('components.json'))
    except Exception as e: 
        print(e)  
        #OR the following to show error message 
        return render_template('home.html', filter=cybervision.Filter().to_json(), flows=[], error=False, errormessage="CUSTOMIZE: Add custom message here.", errorcode=e, deadline=0)

@app.route('/flows', methods=["GET", "POST"])
def flows():
    global FILTER

    page = int(request.args.get('page'))
    deadline = int(request.args.get('deadline'))
    start = page*FLOWS_PER_PAGE
    flows = getJson('flows.json')
    total = int(math.ceil(len(flows)/FLOWS_PER_PAGE))
    nextpage = page
    previouspage = page
    flows = flows[start:start+FLOWS_PER_PAGE]
    if len(flows) == FLOWS_PER_PAGE and total>page:
        nextpage = page+1
    else:
        nextpage = 0
    if page == 0:
        previouspage = total
    else: 
        previouspage = page-1

    return render_template('home.html', filter=FILTER.to_json(), flows=flows, previouspage=previouspage, nextpage=nextpage, total=total, deadline=deadline, label_list=getJson('components.json'))

@app.route('/ip-addresses', methods=["GET", "POST"])
def ips():
    label = request.args.get('label')
    ips = cybervision.get_ips(label)
    return ', '.join(ips)

@app.route('/csv', methods=["GET"])
def get_csv():
    make_csv()
    return flask_send_file('flows.csv')

def get_days_since(unixtime):
    then = datetime.datetime.fromtimestamp(unixtime)
    now = datetime.datetime.now()
    diff = now-then
    return diff.days

def make_csv():
    with open("flows.csv", "w") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(["Source", "Destination", "Protocol", "Tags", "Last Seen"])
        for f in getJson('flows.json'):
            row = [
                f['source'],
                f['dest'],
                f['sourceport'],
                f['destport'],
                f['protocol'],
                f['tags'],
                f"{f['dayssince']} days ago",
            ]
            writer.writerow(row)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888, debug=True)