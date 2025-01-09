from app import db
from datetime import datetime

class Vehicle(db.Model):
    __tablename__ = 'vehicles'

    vehicle_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    make = db.Column(db.String(50), nullable=False)  # e.g., Toyota
    model = db.Column(db.String(50), nullable=False)  # e.g., Camry
    year = db.Column(db.Integer, nullable=False)  # e.g., 2020
    license_plate = db.Column(db.String(20), unique=True, nullable=False)
    color = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Vehicle {self.make} {self.model} for User {self.user_id}>"