from app import db
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField


class Location(db.Model):
    """Database model for the location of the barge"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, unique=True)
    latitude = db.Column(db.FLOAT(10))
    longitude = db.Column(db.FLOAT(10))

    def __repr__(self):
        str({'datetime' : self.timestamp, 'latitude' : self.latitude, 'longitude': self.longitude})

class QueryForm(FlaskForm):
    quantity = IntegerField('Quantity')
    submit = SubmitField('View Locations')
