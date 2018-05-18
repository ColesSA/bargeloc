import datetime
import json
import time
from urllib.parse import quote_plus

import dataset
import requests
from bs4 import BeautifulSoup

import pyodbc

# Config json reference
with open("./config.json", 'r') as stream:
    config = json.load(stream)

# Populate local lists with config data
web = [str(i[1]) for i in config['WEB'].items()]
dat = [str(i[1]) for i in config['DATABASE'].items()]

# Page request
request = requests.get(web[0], verify=False, auth=(web[2], web[3]))
# NOTE: I would like to get the verification working but I need a valid CA bundle.

# Page data parse
page_data = BeautifulSoup(request.content, 'html.parser')

# Populate local latitude and longitude
lat = page_data.find('div', {'id': 'latlong'})['data-latitude']
lon = page_data.find('div', {'id': 'latlong'})['data-longitude']

# Current time to use as timestamp
time = datetime.datetime.fromtimestamp(
    time.time()).strftime('%Y-%m-%d %H:%M:%S')

# Connect to the database; form object reference
db = dataset.connect(
    'mssql+pyodbc:///?odbc_connect=%s' %
    quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + dat[0] +
               ';DATABASE=' + dat[1] + ';UID=' + dat[2] + ';PWD=' + dat[3]))

# Insert table to database
db['location'].insert({'timestamp': time, 'latitude': lat, 'longitude': lon})
