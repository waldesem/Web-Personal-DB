from flask import Flask

from config import Config
from .routes.route import bp as route_bp
from .cors.extension import CORS


app = Flask(__name__)

app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

app.register_blueprint(route_bp)
