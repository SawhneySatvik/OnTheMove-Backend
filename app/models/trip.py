from app import db
from datetime import datetime

class Trip(db.Model):
    __tablename__ = 'trips'

    trip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.ride_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    status = db.Column(db.String(50), default='requested')  # requested, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Trip {self.trip_id} for Ride {self.ride_id} by User {self.user_id}>"