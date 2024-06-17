from flask import Flask

from app.routes import bp as route_bp
from .cors.extension import CORS
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

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
