import json
from urllib.parse import quote_plus
import os

# Config json references
with open("./config.json", 'r') as stream:
    config = json.load(stream)

URL = config['URL']
UID = config['UID']
PWD = config['PWD']
SERVER = config['SERVER']
DB = config['DB']

db_url = quote_plus('DRIVER={ODBC Driver 13 for SQL Server};SERVER=' + SERVER +
                    ';DATABASE=' + DB + ';UID=' + UID + ';PWD=' + PWD)


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc:///?odbc_connect=%s' % db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
