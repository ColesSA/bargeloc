import urllib3
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

# Temporary muting of requests verification error
#urllib3.disable_warnings()

app = Flask(__name__)
app.config.from_object(Config)
# Connect to the database
db = SQLAlchemy(app)

from app import routes, models
