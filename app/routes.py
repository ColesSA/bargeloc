from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import redirect, render_template, request, url_for

from app import app, db
<<<<<<< HEAD
from app.models import Location, QueryForm
=======
from app.models import Location, QueryForm, UpdateForm
>>>>>>> parent of ad9ae90... Routing Restructuring and Database Call Rework
from config import PWD, UID, URL


def get_page():
    with requests.get(URL, verify=False, auth=(UID, PWD)) as req:
        return BeautifulSoup(req.content, 'html.parser').find(
            'div', {'id': 'latlong'})


<<<<<<< HEAD
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
=======
# NOTE: I would like to get the verification working but I need a valid CA bundle.


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    if "store" in request.form:
        return redirect(url_for('add'))
    return render_template('base.html', title='Barge Location API')


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>That page could not be found.</p>", 404


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


@app.route('/api/menu', methods=['GET', 'POST'])
def api_menu():
>>>>>>> parent of ad9ae90... Routing Restructuring and Database Call Rework
    form = QueryForm()
    if request.method == 'POST':
        if form.validate() == False:
            return redirect(url_for('list_all'))
        else:
            return redirect(
                url_for('list_q', quantity=request.form['quantity']))
    elif request.method == 'GET':
        return render_template('menu.html', title='Barge Location API', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="404"), 404


<<<<<<< HEAD
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
=======
@app.route('/api/list/all', methods=['GET'])
def list_all():
    locations = db.session.query(Location).all()
    return render_template('locations.html', title='Data', locations=locations)


@app.route('/api/list/last', methods=['GET'])
def list_last():
    return redirect(url_for('list_q', quantity=1))


@app.route('/api/list/<int:quantity>', methods=['GET'])
def list_q(quantity):
    quantity = 1 if (quantity == None) else int(quantity)
    locations = db.session.query(Location).all()[(quantity * -1):]
    return render_template('locations.html', title='Data', locations=locations)
>>>>>>> parent of ad9ae90... Routing Restructuring and Database Call Rework
