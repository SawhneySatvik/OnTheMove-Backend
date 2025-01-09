from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Config


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return '<h1>Hello</h1>'

from app.blueprints import auth_bp
app.register_blueprint(auth_bp)