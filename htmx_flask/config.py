from configparser import ConfigParser
import os

basedir = os.path.abspath(os.path.dirname(__file__))
setting = ConfigParser()
setting.read(os.path.join(basedir, "settings.ini"))


class Config:
    SECRET_KEY = "SUPERSECRETKEY"
    BASE_PATH = (
        setting["Destination"].get("path")
        if setting["Destination"].get("path")
        else os.path.join(basedir, "..", "PersonalDB")
    )
    DEFAULT_PASSWORD = "8" * 8
    DATABASE_URI = (
        os.path.join("sqlite:///", setting["SQLite"].get("uri"), "database.db")
        if setting["SQLite"].get("uri")
        else os.path.join("sqlite:///", "..", "database.db")
    )
