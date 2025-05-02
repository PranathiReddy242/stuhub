import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-secret-key-2023'
    DATABASE = 'stuhub.db'