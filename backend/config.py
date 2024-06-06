import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_URI = os.path.abspath(os.path.join("..", 'database.db'))
    DATABASE_SQL = os.path.abspath(os.path.join("..", "database.sql"))
    BASE_PATH = os.path.abspath(os.path.join("..", "persons"))
    DEFAULT_PASSWORD = "8" * 8
    PAGINATION = 16
