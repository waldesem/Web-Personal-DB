"""Initialize the Flask application."""

from __future__ import annotations

from flask import Flask, Response
from werkzeug.exceptions import HTTPException

from app.model.tables import db_session
from app.utils.compress import Compress
from config import Config, handler


def create_app(config_class: Config = Config) -> Flask:
    """Create and configure the Flask application.

    Args:
        config_class: The configuration class to use for the application.

    Returns:
        Flask: The configured Flask application instance.

    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.logger.addHandler(handler)

    compress = Compress()
    compress.init_app(app)

    from app.routes import bp as route_bp
    from command import bp as command_bp

    app.register_blueprint(route_bp)
    app.register_blueprint(command_bp)

    @app.teardown_appcontext
    def shutdown_session(
        exception: Exception | None = None,  # noqa: ARG001
    ) -> None:
        """Close the database session after each request or exception."""
        db_session.remove()

    @app.get("/", defaults={"path": ""})
    def main(path: str = "") -> str:  # noqa: ARG001
        return app.send_static_file("index.html")

    @app.get("/<path:path>")
    def static_file(path: str = "") -> str:
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
