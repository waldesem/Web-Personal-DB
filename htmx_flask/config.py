from configparser import ConfigParser
import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))
setting = ConfigParser()
setting.read(os.path.join(basedir, "settings.ini"))


class Configuration:
    SECRET_KEY = "secrets.token_hex(16)"
    BASE_PATH = (
        setting["Destination"].get("path")
        if setting["Destination"].get("path")
        else os.path.join(basedir, "PersonalDB")
    )
    DEFAULT_PASSWORD = "8" * 8
    DATABASE_URI = (
        os.path.join("sqlite:///", setting["SQLite"].get("uri"), "database.db")
        if setting["SQLite"].get("uri")
        else os.path.join("sqlite:///database.db")
    )


class DesktopConfig(Configuration):
    SECRET_KEY = "SUPERSECRETKEY"


class SqliteServerConfig(Configuration):
    pass


class PostgreServerConfig(Configuration):
    DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        setting["Postgre"]["user"],
        setting["Postgre"]["password"],
        setting["Postgre"]["host"],
        setting["Postgre"]["port"],
        setting["Postgre"]["dbname"],
    )


class Config(SqliteServerConfig):
    pass
