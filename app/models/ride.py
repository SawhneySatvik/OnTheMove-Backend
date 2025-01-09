from app import db
from datetime import datetime

class Ride(db.Model):
    __tablename__ = 'rides'

    ride_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    start_location = db.Column(db.String(255), nullable=False)
    start_latitude = db.Column(db.Float, nullable=False)
    start_longitude = db.Column(db.Float, nullable=False)
    end_location = db.Column(db.String(255), nullable=False)
    end_latitude = db.Column(db.Float, nullable=False)
    end_longitude = db.Column(db.Float, nullable=False)
    date_and_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), default='active')  # active, completed, canceled
    cost = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    trips = db.relationship('Trip', backref='ride', lazy=True)
    ratings = db.relationship('Rating', backref='ride', lazy=True)

    def __repr__(self):
        return f"<Ride {self.ride_id} by User {self.user_id}>"