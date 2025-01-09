from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    profile_picture = db.Column(db.String(255), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    verification_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    rides = db.relationship('Ride', backref='creator', lazy=True)
    trips = db.relationship('Trip', backref='user', lazy=True)
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)
    frequent_locations = db.relationship('FrequentLocation', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"