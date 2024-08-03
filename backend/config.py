from configparser import ConfigParser
import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))
setting = ConfigParser()
setting.read(os.path.join(basedir, "settings.ini"))


class Config:
    SECRET_KEY = "secrets.token_hex(16)"
    SQLITE_URI = (
        f"sqlite:///{setting['SQLite'].get('uri')}/database.db"
        if setting["SQLite"].get("uri")
        else os.path.join("sqlite:///database.db")
    )
    POSTGRE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        setting["Postgre"]["user"],
        setting["Postgre"]["password"],
        setting["Postgre"]["host"],
        setting["Postgre"]["port"],
        setting["Postgre"]["dbname"],
    )
    DATABASE_URI = SQLITE_URI
    BASE_PATH = (
        setting["Destination"].get("path")
        if setting["Destination"].get("path")
        else os.path.join(basedir, "..", "persons")
    )
    DEFAULT_PASSWORD = "8" * 8
