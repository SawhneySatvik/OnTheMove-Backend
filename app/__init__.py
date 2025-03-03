from flask import Flask, request
from flask.json import jsonify

from app.config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from supabase import create_client
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object(Config)

supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.before_request
def handle_options_request():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        return response

@app.route("/")
def hello():
    return jsonify({"message": "Hello, world!"})

from app.blueprints import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")