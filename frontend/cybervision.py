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

class Filter():
    def __init__(self, source_ip=None, dest_ip=None, from_date=None, to_date=None):
        if source_ip == "":
            source_ip = None
        self.source_ip = source_ip

        if dest_ip == "":
            dest_ip = None
        self.dest_ip = dest_ip

        if from_date == "" or from_date is None:
            self.from_date = datetime.datetime.today() - datetime.timedelta(days=7)
        else:
            datetimeobject = datetime.datetime.strptime(from_date, "%Y-%m-%d")
            self.from_date = datetimeobject

        if to_date == "" or to_date is None:
            self.to_date = datetime.datetime.today()
        else:
            datetimeobject = datetime.datetime.strptime(to_date, "%Y-%m-%d")
            self.to_date = datetimeobject
    
    def get_query_string(self):
        query = ""
        if self.from_date is not None:
            query += f"&from={self.from_date.strftime('%s')}000"
        if self.to_date is not None:
            query += f"&to={self.to_date.strftime('%s')}000"
        
        if len(query) == 0:
            return query
        else:
            return query[1:]
    
    def to_json(self):
        return {
            "sourceip" : self.source_ip if self.source_ip is not None else "",
            "destip" : self.dest_ip if self.dest_ip is not None else "",
            "fromdate" : self.from_date.strftime("%Y-%m-%d") if self.from_date is not None else None,
            "todate" : self.to_date.strftime("%Y-%m-%d") if self.to_date is not None else None,
        }
    
    def from_json(json_object):
        return Filter(
            source_ip=json_object['sourceip'],
            dest_ip=json_object['destip'],
            from_date=json_object['fromdate'],
            to_date=json_object['todate']
        )

def get_all_flows(filter=None):
    host = os.environ['CYBERVISION_HOST']
    token = os.environ['CYBERVISION_TOKEN']

    url = f"https://{host}/api/3.0/flows?{filter.get_query_string()}"
    print(f"Making api request to: {url}")

    headers = {
        "Accept" : "application/json",
        "x-token-id" : token
    }

    flows = requests.get(url, headers=headers, verify=False).json()

    # Source/dest filter
    result = []
    if filter.source_ip is not None:
        for f in flows:
            if f['left']['label'] in filter.source_ip:
                result += [f]
    else:
        result = flows
    result_result = []
    if filter.dest_ip is not None:
        for f in result:
            if f['right']['label'] in filter.dest_ip:
                result_result += [f]
    else:
        result_result = result
    
    result_after_ips = result_result

    return result_after_ips

# get components 
def get_components():
    host = os.environ['CYBERVISION_HOST']
    token = os.environ['CYBERVISION_TOKEN']

    url = f"https://{host}/api/3.0/components"

    headers = {
        "Accept" : "application/json",
         "x-token-id" : token
    }
    list=[]
    components = requests.get(url, headers=headers, verify=False).json()

    for comp in components:
        for i in comp['otherProperties']:
            if i['key'] == os.environ['FILTER_TAG']: #pretend this is cybervision-pov
                list.append({"name": i['value']}) #get the different values e.g AMP client, and append to the list
    #Remove the duplicates from list
    seen = set()
    new_l = []
    for d in list:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)
    list=new_l

    return sorted(list, key = lambda i:i['name'])

#Pass the selected property here
def get_ips(property):
    host = os.environ['CYBERVISION_HOST']
    token = os.environ['CYBERVISION_TOKEN']
    url = f"https://{host}/api/3.0/components"
    list_of_ips=[]
    headers = {
        "Accept" : "application/json",
         "x-token-id" : token
    }
    components = requests.get(url, headers=headers, verify=False).json()
    for comp in components:
        for i in comp['otherProperties']:
            if i['key'] == os.environ['FILTER_TAG'] and i['value'] == property:
                if comp['ip']: #get rid of empty strings, some comps don't have ip set
                    list_of_ips.append(comp['ip'])
    return list_of_ips

def get_names(property):
    host = os.environ['CYBERVISION_HOST']
    token = os.environ['CYBERVISION_TOKEN']
    url = f"https://{host}/api/3.0/components"
    list_of_names=[]
    headers = {
        "Accept" : "application/json",
         "x-token-id" : token
    }
    components = requests.get(url, headers=headers, verify=False).json()
    for comp in components:
        for i in comp['otherProperties']:
            if i['key'] == os.environ['FILTER_TAG'] and i['value'] == property:
                if comp['device']:
                    list_of_names.append(comp['device']['label'])
    return list_of_names

if __name__ == "__main__":
    load_dotenv()
    