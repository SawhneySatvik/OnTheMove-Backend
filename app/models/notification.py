from app import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # e.g., Ride Update, Chat Message
    content = db.Column(db.Text, nullable=False)
    read_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Notification {self.notification_type} for User {self.user_id}>"