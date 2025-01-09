from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, decode_token, jwt_required
from datetime import timedelta
from functools import wraps
from flask import jsonify, request

def create_tokens(identity):
    """
    Create access and refresh tokens for a given identity.

    Args:
        identity (str): Identity of the user (e.g., user details as a string or JSON).
    
    Returns:
        dict: Access and refresh tokens.
    """
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

def extract_user_id_from_token():
    """
    Extract the user ID from the JWT token.

    Returns:
        tuple: (User ID, HTTP status code) or error response.
    """
    identity = get_jwt_identity()
    if not identity:
        return jsonify({"message": "Access denied. Missing or invalid token."}), 401
    
    try:
        # Extract user ID from the identity (assuming identity contains `id` field)
        identity_parts = dict(item.split(":") for item in identity.split(","))
        user_id = identity_parts.get("id")

        if user_id:
            return user_id, 200
        else:
            return jsonify({"message": "User not found"}), 403
    except Exception:
        return jsonify({"message": "Invalid token structure"}), 400

def roles_required(allowed_roles):
    """
    Role-based access control decorator.

    Args:
        allowed_roles (list): List of roles that can access the endpoint.

    Returns:
        function: Wrapped function with role validation.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if not identity:
                return jsonify({"message": "Access denied. Missing or invalid token."}), 401

            try:
                # Extract role from identity (assuming identity contains `role` field)
                identity_parts = dict(item.split(":") for item in identity.split(","))
                role = identity_parts.get("role")

                if role not in allowed_roles:
                    return jsonify({"message": f"Access denied. Allowed roles: {', '.join(allowed_roles)}"}), 403

                return fn(*args, **kwargs)
            except Exception:
                return jsonify({"message": "Invalid token structure"}), 400
        return wrapper
    return decorator

def decode_jwt(token):
    """
    Decode a JWT token.

    Args:
        token (str): JWT token.
    
    Returns:
        dict: Decoded token data.
    """
    return decode_token(token)

def get_current_user():
    """
    Get the current user's identity from the token.

    Returns:
        str: User identity.
    """
    return get_jwt_identity()

def driver_required(fn):
    """
    Decorator to restrict access to drivers only.

    Args:
        fn (function): Function to wrap.

    Returns:
        function: Wrapped function.
    """
    return roles_required(["driver"])(fn)

def rider_required(fn):
    """
    Decorator to restrict access to riders only.

    Args:
        fn (function): Function to wrap.

    Returns:
        function: Wrapped function.
    """
    return roles_required(["rider"])(fn)

def admin_required(fn):
    """
    Decorator to restrict access to admins only.

    Args:
        fn (function): Function to wrap.

    Returns:
        function: Wrapped function.
    """
    return roles_required(["admin"])(fn)