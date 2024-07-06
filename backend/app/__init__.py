from flask import Flask

# from flask_cors import CORS

from config import Config
from .routes.route import bp as route_bp


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)

    # CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    app.register_blueprint(route_bp)

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