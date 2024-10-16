from configparser import ConfigParser
import os
import secrets


basedir = os.path.abspath(os.path.dirname(__file__))
setting = ConfigParser()
setting.read(os.path.join(basedir, "settings.ini"), encoding="utf-8")


class Configuration:
    SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY = secrets.token_hex(16)
    BASE_PATH = setting["Destination"].get("path")
    DATABASE_URI = "".join(["sqlite:///", os.path.join(BASE_PATH, "database.db")])
    DEFAULT_PASSWORD = "8" * 8


class SqliteConfig(Configuration):
    pass


class DesktopConfig(Configuration):
    SECRET_KEY = "secret_key"
    JWT_SECRET_KEY = "jwt_secret_key"


class PostgreConfig(Configuration):
    DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        setting["Postgre"]["user"],
        setting["Postgre"]["password"],
        setting["Postgre"]["host"],
        setting["Postgre"]["port"],
        setting["Postgre"]["dbname"],
    )


class Config(DesktopConfig):
    pass
