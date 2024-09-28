from configparser import ConfigParser
import os
import secrets


basedir = os.path.abspath(os.path.dirname(__file__))
setting = ConfigParser()
setting.read(os.path.join(basedir, "settings.ini"), encoding="utf-8")


class Configuration:
    SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY = secrets.token_hex(16)
    BASE_PATH = (
        setting["Destination"].get("path")
        if setting["Destination"].get("path")
        else os.path.join(basedir, "PersonalDB")
    )
    DEFAULT_PASSWORD = "8" * 8
    DATABASE_URI = (
        "sqlite:///" + os.path.join(setting["SQLite"].get("uri"), "database.db")
        if setting["SQLite"].get("uri")
        else os.path.join("sqlite:///", "database.db")
    )


class SqliteConfig(Configuration):
    pass


class PostgreConfig(Configuration):
    DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        setting["Postgre"]["user"],
        setting["Postgre"]["password"],
        setting["Postgre"]["host"],
        setting["Postgre"]["port"],
        setting["Postgre"]["dbname"],
    )


class Config(SqliteConfig):
    pass
