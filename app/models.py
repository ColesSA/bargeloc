from app import db

class Location(db.Model):
    """Database model for the location of the barge"""
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, unique=True)
    latitude = db.Column(db.FLOAT(10))
    longitude = db.Column(db.FLOAT(10))

    def __repr__(self):
        return '<{}:({},{})>'.format(self.timestamp, self.latitude, self.longitude)   

