"""Initialize the Flask application."""

from __future__ import annotations

import logging

from flask import Flask, Response
from werkzeug.exceptions import HTTPException

from app.extensions.caching import Cache
from app.extensions.compress import Compress
from app.extensions.database import Database
from app.extensions.revoking import RevokeDB
from config import Config

handler = logging.FileHandler("error.log", mode="w", encoding="utf-8")
handler.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

caching = Cache()  # Create the caching instance
compress = Compress()  # Create the compression instance
db = Database()  # Create the database instance for SQLAlchemy
revoked = RevokeDB()  # Create the database instance for revoked tokens

def create_app(config_class: Config = Config) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.logger.addHandler(handler)

    compress.init_app(app)  # Initialize the compression
    db.init_app(app)  # Initialize the database

    from app.routes import bp as route_bp  # noqa: PLC0415
    from command import bp as command_bp  # noqa: PLC0415

    app.register_blueprint(route_bp)  # Register the routes
    app.register_blueprint(command_bp)  # Register the commands

    @app.get("/")
    def main() -> Response:
        """Return the main page."""
        return app.send_static_file("index.html")

    @app.get("/<path:path>")
    def static_file(path: str) -> Response:
        """Return a static file."""
        return app.send_static_file(path)

    @app.errorhandler(404)
    def handle_404(error: HTTPException) -> Response:
        app.logger.exception(error)
        return app.redirect("/")

    @app.errorhandler(HTTPException)
    def handle_exception(error: HTTPException) -> Response:
        app.logger.exception(error)
        return error

    return app
