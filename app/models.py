from app import db
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired


class Location(db.Model):
    """Database model for the location of the barge"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, unique=True)
    latitude = db.Column(db.FLOAT(10))
    longitude = db.Column(db.FLOAT(10))

    def __repr__(self):
        return u'<datetime={}:(latitude={}, longitude={})>'.format(
            self.timestamp, self.latitude, self.longitude)


class QueryForm(FlaskForm):
    quantity = IntegerField('Quantity')
    submit = SubmitField('View Locations')


class UpdateForm(FlaskForm):
    submit = SubmitField('Store Current Location')
