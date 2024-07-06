import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))
    

class Config:
    SECRET_KEY = secrets.token_hex(16)
    DATABASE_URI = os.path.join(basedir, "..", 'database.db')
    BASE_PATH = os.path.join(basedir, "..", "persons")
    DEFAULT_PASSWORD = "8" * 8
