from flask import request, jsonify
from app.blueprints.auth import auth_bp
from app.services.auth import register_user, login_user

@auth_bp.route('/')
def auth_home():
    return '<h1>From authentication route</h1>'

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error':"Request body must be JSON"}),400
    response, status = register_user(data)
    return response, status

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error':"Request body must be JSON"}),400
    response, status = login_user(data)
    return response, status

@auth_bp.route('/verify', methods=['POST'])
def verify():
    return '<h1>Verfication thought mobile number or email Route</h1>'

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return '<h1>Logout Route</h1>'

@auth_bp.route('/profile', methods=['GET', 'PUT'])
def handle_profile():
    return '<h1>Handle Profile Route</h1>'

@auth_bp.route('/delete', methods=['DELETE'])
def delete():
    return '<h1>Delete</h1>'

