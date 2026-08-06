from extensions import db
from flask_login import UserMixin
from datetime import datetime, timezone

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    pass_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='active',nullable=False)

    staff_profile = db.relationship('TrekStaff', backref='user', uselist=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)


class TrekStaff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_num = db.Column(db.String(100))
    exp = db.Column(db.Text)
    approval = db.Column(db.Boolean, default=False)

class Trek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20)) # Easy | Moderate | Hard
    duration = db.Column(db.Integer) #number of days trek will last
    available_slots = db.Column(db.Integer, default=0)
    assinged_staff_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending | Approved | Open | Closed | Completed
    start_date = db.Column(db.Date)
    emd_date = db.Column(db.Date)

    assinged_staff = db.relationship('User', foreign_keys=[assinged_staff_id])
    booking = db.relationship('Booking', backref='trek', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='Booked') #Booked | Completed | Cancelled