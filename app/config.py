import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    SECRET_KEY = os.environ.get("SECRET_KEY", "satvik_secret_key")
    
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://rfzprstdtggqshfeejla.supabase.co")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "ISSUE_KEY")
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///on_the_move_default.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "satvik_jwt_secret_key")
