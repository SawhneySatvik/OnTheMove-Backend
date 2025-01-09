from flask import request, jsonify
from app.blueprints.auth import auth_bp

@auth_bp.route('/')
def auth_home():
    return '<h1>From authentication route</h1>'

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return data.jsonify()

@auth_bp.route('/login', methods=['POST'])
def login():
    return '<h1>Login Route</h1>'

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

