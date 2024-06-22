import os
# import secrets

basedir = os.path.abspath(os.path.dirname(__file__))
    

class Config:
    SECRET_KEY = "secrets.token_hex(16)"
    DATABASE_URI = os.path.abspath(os.path.join("..", 'database.db'))
    DATABASE_SQL = os.path.abspath(os.path.join("..", "database.sql"))
    BASE_PATH = os.path.abspath(os.path.join("..", "persons"))
    DEFAULT_PASSWORD = "8" * 8
    PAGINATION = 16
