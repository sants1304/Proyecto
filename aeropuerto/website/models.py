from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role = db.Column(db.String(100))
    dob = db.Column(db.String(100))
    nationality = db.Column(db.String(100))
    contact_no = db.Column(db.String(100))
    address = db.Column(db.String(100))

class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airline = db.Column(db.String(100))
    origin = db.Column(db.String(100))
    dest = db.Column(db.String(100))
    date = db.Column(db.String(100))
    dept_time = db.Column(db.String(100))
    arr_time = db.Column(db.String(100))
    pilotid = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    status = db.Column(db.String(100))

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    date = db.Column(db.String(100))
    people = db.Column(db.Integer)
    flightid = db.Column(db.Integer)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    subject = db.Column(db.String(10000))
    comment = db.Column(db.String(100000000))