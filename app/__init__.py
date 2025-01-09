from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Config


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return jsonify({'message':'There will be data here'})

from app.blueprints import auth_bp
app.register_blueprint(auth_bp)