import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///on_the_move.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False