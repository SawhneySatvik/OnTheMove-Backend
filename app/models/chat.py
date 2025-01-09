from app import db
from datetime import datetime

class Chat(db.Model):
    __tablename__ = 'chats'

    chat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ride_id = db.Column(db.Integer, db.ForeignKey('rides.ride_id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Chat from User {self.sender_id} in Ride {self.ride_id}>"