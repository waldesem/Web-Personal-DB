from flask import Flask

from .cors.extension import CORS
from config import Config

def create_app(config=Config):
    """
    Initializes and configures a Flask application. 
    """
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    from app.routes import bp as route_bp

    app.register_blueprint(route_bp)

    from cli import register_cli

    register_cli(app)

    @app.get("/", defaults={"path": ""})
    def main(path=""):
        return app.send_static_file("index.html")
    
    @app.get("/<path:path>")
    def static_file(path=""):
        return app.send_static_file(path)

    @app.errorhandler(404)
    def not_found(error):
        return app.redirect("/")

    return app
