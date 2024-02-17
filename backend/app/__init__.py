from apiflask import APIFlask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_jwt_extended import JWTManager

from config import Config

db = SQLAlchemy()
cache = Cache()
jwt = JWTManager()


def create_app(config=Config):
    """
    Initializes and configures a Flask application.
    """
    app = APIFlask(__name__, title="StaffSec", docs_ui="redoc")
    app.config.from_object(config)
    # app.config['REDOC_STANDALONE_JS'] = './static/redoc.standalone.js'
    # for local use, download redoc.standalone.js
    # from https://github.com/Redocly/redoc/blob/master/redoc/static/redoc.standalone.js
    # and save it in the static folder or in frontend/public

    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db, render_as_batch=True)

    from app.routes.anketa import bp_anketa as anketa_bp

    app.register_blueprint(anketa_bp)

    from app.routes.checks import bp_checks as checks_bp

    app.register_blueprint(checks_bp)

    from app.routes.classes import bp_classify as classify_bp

    app.register_blueprint(classify_bp)

    from app.routes.contacts import bp_contact as contacts_bp

    app.register_blueprint(contacts_bp)

    from app.routes.files import bp_files as files_bp

    app.register_blueprint(files_bp)

    from app.routes.login import bp_login as login_bp

    app.register_blueprint(login_bp)

    from app.routes.manager import bp_manager as manager_bp

    app.register_blueprint(manager_bp)

    from app.routes.messages import bp_message as message_bp

    app.register_blueprint(message_bp)

    from app.routes.person import bp_persons as persons_bp

    app.register_blueprint(persons_bp)

    from app.routes.resume import bp_resume as resume_bp

    app.register_blueprint(resume_bp)

    from cli import register_cli

    register_cli(app)

    @app.get("/", defaults={"path": ""})
    @app.get("/<path:path>")
    @app.doc(hide=True)
    @cache.cached()
    def main(path=""):
        return app.send_static_file("index.html")

    @app.error_processor
    def flask_error_processor(error):
        return (
            {
                "status_code": error.status_code,
                "message": error.message,
                "detail": error.detail,
            },
            error.status_code,
            error.headers,
        )

    return app
