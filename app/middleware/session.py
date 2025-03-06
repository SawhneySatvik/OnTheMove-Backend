from flask import request, jsonify
from app import supabase
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = request.headers.get("Authorization")
        refresh_token = request.headers.get("Refresh-Token")
        if not access_token or not access_token.startswith("Bearer ") or not refresh_token:
            return jsonify({"error": "Access token or refresh token missing"}), 401
        try:
            access_token = access_token.split(" ")[1]
            supabase.auth.set_session(access_token, refresh_token)
            user = supabase.auth.get_user()
            print(f"Authenticated user: {user.user.id}")  # Debug
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": f"Invalid token: {str(e)}"}), 401
    return decorated