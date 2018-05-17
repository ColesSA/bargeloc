import json
import requests
from bs4 import BeautifulSoup

with open("./config.json", 'r') as stream:
        config = json.load(stream)

 # This section will be changed later to something less crap 
 # once it works and I do some learning on python lists.

 # Populate local vars with config data 
url = config['WEB']['URL']
web_user = config['WEB']['USER']
web_pass = config['WEB']['PASSWRD']

db = config['DATABASE']['DB']
db_host = config['DATABASE']['HOST']
db_user = config['DATABASE']['USER']
db_pass = config['DATABASE']['PASSWRD']


 # get the page data
page = requests.get(url, verify=False, auth=(web_user, web_pass))
page_data = BeautifulSoup(page.content, 'html.parser')

 # populate latitude and longitude vars with values
lat = page_data.find('div',{'id' : 'latlong'})['data-latitude']
lon = page_data.find('div',{'id' : 'latlong'})['data-longitude']

 # make list, because
latlon = [lat,lon]

print(latlon)