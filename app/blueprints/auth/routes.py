from flask import request, jsonify
from app import supabase

from . import auth_bp

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.
    Expects: { "name": str, "email": str, "password": str }
    Returns: Access token, refresh token, and user ID on success.
    """
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        user = supabase.auth.sign_up({"email": email, "password": password})
        user_data = {
            "id": user.user.id,
            "email": email,
            "name": name,
            "role": "user",
            "verified": False,
            "created_at": "now()"
        }
        supabase.table("users").insert(user_data).execute()

        return jsonify({
            "message": "User registered successfully",
            "access_token": user.session.access_token,
            "refresh_token": user.session.refresh_token,
            "user_id": user.user.id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Log in an existing user.
    Expects: { "email": str, "password": str }
    Returns: Access token, refresh token, and user ID on success.
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        session = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return jsonify({
            "message": "Login successful",
            "access_token": session.session.access_token,
            "refresh_token": session.session.refresh_token,
            "user_id": session.user.id
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401