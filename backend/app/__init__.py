import os
import asyncio

from quart import Quart
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from quart import send_from_directory
from werkzeug.exceptions import BadRequest

from config import Config

ma = Marshmallow()
cache = Cache()
jwt = JWTManager()

loop = asyncio.get_event_loop()

def create_app(config_class=Config):
    app = Quart(__name__)
    app.config.from_object(config_class)
    app.config['REDOC_STANDALONE_JS'] = './static/redoc.standalone.js'
    app.json.sort_keys = False
    
    CORS(app, resources={r"/*": {"origins": "*"}})
    ma.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    
    from app.routes import bp as route_bp
    app.register_blueprint(route_bp)

    from cli import register_cli
    register_cli(app)

    @app.get('/', defaults={'path': ''})
    @app.get('/<path:path>')
    @app.doc(hide=True)
    def main(path=''):
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        
        return app.send_static_file('index.html')

    @app.errorhandler(BadRequest)
    def handle_bad_request(e):
        return e, 400
    
    return app