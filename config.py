import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///books2.db'  # Change to your preferred database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secret_key'
