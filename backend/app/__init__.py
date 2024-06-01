from flask import Flask

from cors import CORS
from config import Config

def create_app(config=Config):
    """
    Initializes and configures a Flask application. 
    """
    app = Flask()
    app.config.from_object(config)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    from app.routes import bp as route_bp

    app.register_blueprint(route_bp)

    from cli import register_cli

    register_cli(app)

    @app.get("/", defaults={"path": ""})
    @app.doc(hide=True)
    def main(path=""):
        return app.send_static_file("index.html")
    
    @app.get("/<path:path>")
    @app.doc(hide=True)
    def static_file(path=""):
        return app.send_static_file(path)

    @app.errorhandler(404)
    def not_found(error):
        return app.redirect("/")

    return app
