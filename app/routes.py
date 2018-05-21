from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import redirect, url_for

from app import app, db
from app.models import Location
from config import URL, UID, PWD

def _p():
    with requests.get(URL, verify=False, auth=(UID,PWD)) as req:
        return BeautifulSoup(req.content, 'html.parser').find('div', {'id': 'latlong'})
# NOTE: I would like to get the verification working but I need a valid CA bundle.

@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return "<h1>Barge Location API</h1><p>This site is a prototype API for managing the location data of the CMoG Glass Barge.</p>"

@app.route('/add', methods=['GET'])
def add():
    page = _p()
    L = Location(timestamp=datetime.now(), latitude=page['data-latitude'], longitude=page['data-longitude'])
    db.session.add(L)
    db.session.commit()
    return redirect(url_for('index'))
