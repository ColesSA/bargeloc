import json
from urllib.parse import quote_plus

# Config json references
with open("./config.json", 'r') as stream:
    config = json.load(stream)

URL = config['URL']
CERT = config['CERT']
UID = config['UID']
PWD = config['PWD']
SERVER = config['SERVER']
DB = config['DB']

db_url = quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + SERVER +
               ';DATABASE=' + DB + ';UID=' + UID + ';PWD=' + PWD)

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc:///?odbc_connect=%s' % db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
