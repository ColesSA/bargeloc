import json
import requests
import dataset
import time, datetime
import pyodbc
import urllib.parse
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

with open("./config.json", 'r') as stream:
        config = json.load(stream)

 # This section will be changed later to something less crap 
 # once it works and I do some learning on python lists.

 # Populate local vars with config data 
web_url = config['WEB']['URL']
web_user = config['WEB']['UID']
web_pass = config['WEB']['PWD']

db_driver = config['DATABASE']['DRIVER']
db_server = config['DATABASE']['SERVER']
db_database = config['DATABASE']['DB']
db_user = config['DATABASE']['UID']
db_pass = config['DATABASE']['PWD']
db_app = config['DATABASE']['APP']

db_dialect = config['test']['dialect']

 # get the time retrieved
time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

 # get the page data
page = requests.get(web_url, verify=False, auth=(web_user, web_pass))
page_data = BeautifulSoup(page.content, 'html.parser')

 # populate latitude and longitude vars with values
lat = page_data.find('div',{'id' : 'latlong'})['data-latitude']
lon = page_data.find('div',{'id' : 'latlong'})['data-longitude']

 # make list, because
latlon = {'timestamp' : time, 'latitude' : lat, 'longitude' : lon}

#print(latlon)

 # form connection string and create the connection
#connString = ("DRIVER={};SERVER={};DATABASE={};UID={};PWD={};APP={}".format(db_driver, db_server, db_database, db_user, db_pass, db_app))
#params = urllib.parse.quote_plus(connString)

 # initialize the database as an object
db = dataset.connect('{}://{}:{}@{}/{}?driver={}'.format(db_dialect,db_user,db_pass,db_server,db_database,db_driver))

table = db['firstTest']
table.insert(latlon)

#conn = pyodbc.connect(r'{}'.format(connString))