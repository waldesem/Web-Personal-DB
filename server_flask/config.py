from configparser import ConfigParser
from datetime import date
import os
import secrets
import shutil

from server_flask.app.model.classes import Regions


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


class DesktopConfig(Configuration):
    SECRET_KEY = "SUPERSECRETKEY"


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


if not os.path.isdir(Config.BASE_PATH):
    os.mkdir(Config.BASE_PATH)
    for region in Regions:
        region_path = os.path.join(Config.BASE_PATH, region.value)
        if not os.path.isdir(region_path):
            os.mkdir(region_path)
        for letter in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ":
            letter_path = os.path.join(region_path, letter)
            if not os.path.isdir(letter_path):
                os.mkdir(letter_path)


if issubclass(Config, SqliteConfig):
    if os.path.isfile(os.path.join(setting["SQLite"].get("uri"), "database.db")):
        if (
            date.fromtimestamp(
                os.path.getmtime(os.path.join(setting["SQLite"].get("uri"), "database.db"))
            ).day
            != date.today().day
        ):
            backup_path = os.path.join(setting["SQLite"].get("uri"), "backup")
            if not os.path.isdir(backup_path):
                os.mkdir(backup_path)
            shutil.copy(
                os.path.join(setting["SQLite"].get("uri"), "database.db"),
                os.path.join(backup_path, f"{date.today()}.db"),
        )
