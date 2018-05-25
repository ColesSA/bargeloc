from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import redirect, render_template, request, url_for, jsonify
from sqlalchemy import func
from sqlalchemy.sql.expression import text

from app import app, db
from app.models import Location, QueryForm
from config import PWD, UID, URL


def get_page():
    with requests.get(URL, verify=False, auth=(UID, PWD)) as req:
        return BeautifulSoup(req.content, 'html.parser').find(
            'div', {'id': 'latlong'})


def loc_factory(locations):
    return {'locations':[{
        'timestamp': loc.timestamp,
        'latitude': loc.latitude,
        'longitude': loc.longitude
    } for loc in locations]}

def coord_factory(locations):
    return {'coords':[{
        'lat': loc.latitude,
        'lng': loc.longitude
    } for loc in locations]}


@app.route('/')
@app.route('/ui/index', methods=['GET', 'POST'])
def index():
    form = QueryForm()
    if request.method == 'POST':
        if form.validate() == False:
            return redirect(url_for('ui_all'))
        else:
            return redirect(url_for('ui_q', quantity=request.form['quantity']))
    elif request.method == 'GET':
        return render_template('menu.html', title='Barge Location API', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="404"), 404


@app.route('/ui/locations', methods=['GET', 'POST'])
def ui_all():
    if request.method == 'GET':
        return render_template('locations.html', title='Data', locations=db.session.query(Location).all())
    elif request.method == 'POST':
        page = get_page()
        L = Location(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            latitude=page['data-latitude'],
            longitude=page['data-longitude'])
        db.session.add(L)
        db.session.commit()


@app.route('/ui/locations/<int:quantity>', methods=['GET'])
def ui_q(quantity):
    max_id = db.session.query(func.max(Location.id)).scalar()
    start = max_id - quantity
    locations = db.session.query(Location).order_by(Location.id).slice(
        start, max_id)
    return render_template('locations.html', title='Data', locations=locations)

@app.route('/ui/map/<int:quantity>',  methods=['GET'])
def ui_m(quantity):
    max_id = db.session.query(func.max(Location.id)).scalar()
    start = max_id - quantity
    locations = db.session.query(Location).order_by(Location.id).slice(
        start, max_id)
    return render_template('map.html', title='Map', locations = loc_factory(locations), coords = coord_factory(locations))


@app.route('/api/locations', methods=['GET'])
def api_all():
    return jsonify(loc_factory(db.session.query(Location).all()))
        

@app.route('/api/locations/now', methods=['GET'])
def api_now():
    page = get_page()
    L = Location(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        latitude=page['data-latitude'],
        longitude=page['data-longitude'])
    db.session.add(L)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/api/locations/<int:quantity>', methods=['GET'])
def api_q(quantity):
    max_id = db.session.query(func.max(Location.id)).scalar()
    start = max_id - quantity
    locations = db.session.query(Location).order_by(Location.id).slice(
        start, max_id)
    return jsonify(dict_factory(locations))
