from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
from datetime import datetime

def set_password(user:User, password):
    hashed_password = generate_password_hash(password)
    user.password = hashed_password
    
def check_password(user:User, password):
    return check_password_hash(user.password, password)

def register_user(data):
    try:
        required_fields = [ 'first_name', 'last_name', 'email', 'phone_number', 'password', 'gender', 'date_of_birth' ]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"errror":f'{field} is required'}), 400
            
        if User.query.filter(User.email==data.get('email')).first():
            return jsonify({'error':"User with this email already exists"}), 400
        
        if User.query.filter(User.phone_number == data.get('phone_number')).first():
            return jsonify({'error':"User with this phone number already exists"}), 400
        
        try:
            date_of_birth = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format for date_of_birth. Use YYYY-MM-DD."}, 400
        
        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone_number=data["phone_number"],
            gender=data["gender"],
            date_of_birth=date_of_birth,
            bio=data.get("bio"),
            profile_picture=data.get("profile_picture")
        )
        
        set_password(new_user,data["password"])
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message':'User registered successfully',
            'user_id':new_user.user_id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message':"user couldn't be created successfully",
            'error':e
        })
        
def login_user(data):
    try:
        if not data.get("email_or_password") or not data.get("password"):
            return jsonify({"error": "email_or_password and password are required"}), 400

        user = User.query.filter(
            (User.email == data.get("email_or_password")) | (User.phone_number == data.get("email_or_password"))
        ).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        if not check_password_hash(user.password, data.get("password")):
            return jsonify({"error": "Invalid password"}), 401

        if not user.verification_status:
            return jsonify({"error": "Account not verified"}), 403

        return jsonify({
            "message": "Login successful",
            "user": {
                "user_id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "role": user.role,
                "profile_picture": user.profile_picture,
                "bio": user.bio,
                "gender": user.gender,
                "date_of_birth": user.date_of_birth.isoformat(),
                "verification_status": user.verification_status,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500