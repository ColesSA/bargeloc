import datetime
import json
import time
from urllib.parse import quote_plus

import dataset
import requests
from bs4 import BeautifulSoup

import pyodbc

with open("./config.json", 'r') as stream:
        config = json.load(stream)

# This section will be changed later to something less crap 
# once it works and I do some learning on python lists.

# Populate local vars with config data 
web_url = config['WEB']['URL']
web_user = config['WEB']['UID']
web_pass = config['WEB']['PWD']

db_server = config['DATABASE']['SERVER']
db_database = config['DATABASE']['DB']
db_user = config['DATABASE']['UID']
db_pass = config['DATABASE']['PWD']

# get the page data
page = requests.get(web_url, verify=False, auth=(web_user, web_pass))
page_data = BeautifulSoup(page.content, 'html.parser')

# populate latitude and longitude vars with values
lat = page_data.find('div',{'id' : 'latlong'})['data-latitude']
lon = page_data.find('div',{'id' : 'latlong'})['data-longitude']

# initialize the database as a dataset object
db = dataset.connect('mssql+pyodbc:///?odbc_connect={}'.format(quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+db_server+';DATABASE='+db_database+';UID='+db_user+';PWD='+db_pass)))

# get the current time to use as time retrieved
time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

# write test table to database
table = db['testTable']
table.insert({'timestamp' : time, 'latitude' : lat, 'longitude' : lon})

# print table to show success
for entry in db['testTable']:
        print(entry)
