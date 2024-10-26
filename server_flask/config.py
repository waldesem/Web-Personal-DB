from configparser import ConfigParser
import os
import secrets


BASE = os.path.abspath(os.path.dirname(__file__))

setting = ConfigParser()
setting.read(os.path.join(BASE, "settings.ini"), encoding="utf-8")


class Configuration:
    SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY = secrets.token_hex(16)
    BASE_PATH = setting["Destination"].get("path")
    DATABASE_URI = "sqlite:///" + os.path.join(BASE_PATH, "database.db")
    DEFAULT_PASSWORD = "88888888"


class SqliteConfig(Configuration):
    pass


class PostgreConfig(Configuration):
    DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        setting["PostgreSQL"]["user"],
        setting["PostgreSQL"]["password"],
        setting["PostgreSQL"]["host"],
        setting["PostgreSQL"]["port"],
        setting["PostgreSQL"]["dbname"],
    )


class Config(SqliteConfig):
    pass
