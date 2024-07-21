import configparser
import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))
setting = configparser.ConfigParser()
setting.read(os.path.join(basedir, "settings.ini"))


class Config:
    SECRET_KEY = "secrets.token_hex(16)"
    SQLITE_URI = os.path.join("sqlite:///database.db")
    POSTGRE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        setting["Postgre"]["user"],
        setting["Postgre"]["password"],
        setting["Postgre"]["host"],
        setting["Postgre"]["port"],
        setting["Postgre"]["dbname"],
    )
    DATABASE_URI = SQLITE_URI
    BASE_PATH = os.path.join(basedir, "..", "persons")
    DEFAULT_PASSWORD = "8" * 8
