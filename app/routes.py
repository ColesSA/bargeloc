from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import redirect, render_template, request, url_for

from app import app, db
from app.models import Location, QueryForm, UpdateForm
from config import PWD, UID, URL


def get_page():
    with requests.get(URL, verify=False, auth=(UID, PWD)) as req:
        return BeautifulSoup(req.content, 'html.parser').find(
            'div', {'id': 'latlong'})


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
    form = QueryForm()
    if request.method == 'POST':
        if form.validate() == False:
            return redirect(url_for('list_all'))
        else:
            return redirect(
                url_for('list_q', quantity=request.form['quantity']))
    elif request.method == 'GET':
        return render_template('menu.html', title='View Locations', form=form)


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
