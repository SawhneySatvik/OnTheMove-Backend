from app import db
from app import app
from app.models.user import User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    admin = User(
        first_name="Satvik",
        last_name="Sawhney",
        email="admin@example.com",
        password=(generate_password_hash('adminsatvik')),
        phone_number="0000000000"
    )
    db.session.add(admin)
    
    db.session.commit()