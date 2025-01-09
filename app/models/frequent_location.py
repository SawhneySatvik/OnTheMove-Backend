from app import db
from datetime import datetime

class FrequentLocation(db.Model):
    __tablename__ = 'frequent_locations'

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    location_name = db.Column(db.String(100), nullable=False)  # e.g., Home, Office
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<FrequentLocation {self.location_name} for User {self.user_id}>"