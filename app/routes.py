from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import redirect, render_template, request, url_for, jsonify
from sqlalchemy import func
from sqlalchemy.sql.expression import text

from app import app, db
from app.models import Location, QueryForm, UpdateForm
from config import PWD, UID, URL, CERT


def get_page():
    with requests.get(URL, verify=False, auth=(UID, PWD)) as req:
        return BeautifulSoup(req.content, 'html.parser').find(
            'div', {'id': 'latlong'})


# NOTE: I would like to get the verification working but I need a valid CA bundle.


def dict_factory(locations):
    return [{
        'timestamp': loc.timestamp,
        'latitude': loc.latitude,
        'longitude': loc.longitude
    } for loc in locations]


@app.route('/')
@app.route('/ui/index', methods=['GET'])
def index():
    if "store" in request.form:
        return redirect(url_for('add'))
    return render_template('base.html', title='Barge Location API')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="404"), 404


@app.route('/ui/menu', methods=['GET', 'POST'])
def ui_menu():
    form = QueryForm()
    if request.method == 'POST':
        if form.validate() == False:
            return redirect(url_for('ui_all'))
        else:
            return redirect(url_for('ui_q', quantity=request.form['quantity']))
    elif request.method == 'GET':
        return render_template('menu.html', title='View Locations', form=form)


@app.route('/ui/locations', methods=['GET'])
def ui_all():
    locations = db.session.query(Location).all()
    return render_template('locations.html', title='Data', locations=locations)


@app.route('/ui/locations/<int:quantity>', methods=['GET'])
def ui_q(quantity):
    max_id = db.session.query(func.max(Location.id)).scalar()
    start = max_id - quantity
    locations = db.session.query(Location).order_by(Location.id).slice(
        start, max_id)
    return render_template('locations.html', title='Data', locations=locations)

@app.route('/ui/map/<int:quantity>',  methods=['GET', 'POST'])
def ui_m(quantity):
    max_id = db.session.query(func.max(Location.id)).scalar()
    start = max_id - quantity
    locations = db.session.query(Location).order_by(Location.id).slice(
        start, max_id)
    return render_template('test.html', title='Map', locations = locations)


@app.route('/api/locations', methods=['GET'])
def api_all():
    locations = db.session.query(Location).all()
    return jsonify(dict_factory(locations))


@app.route('/api/locations/<int:quantity>', methods=['GET'])
def api_q(quantity):
    max_id = db.session.query(func.max(Location.id)).scalar()
    start = max_id - quantity
    locations = db.session.query(Location).order_by(Location.id).slice(
        start, max_id)
    return jsonify(dict_factory(locations))


@app.route('/api/store', methods=['GET'])
def add():
    page = get_page()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    L = Location(
        timestamp=now,
        latitude=page['data-latitude'],
        longitude=page['data-longitude'])
    db.session.add(L)
    db.session.commit()
    return redirect('/')