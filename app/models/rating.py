from app import db
from datetime import datetime

class Rating(db.Model):
    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.ride_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Scale of 1-5
    feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Rating {self.rating} for Ride {self.ride_id} by User {self.user_id}>"