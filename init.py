# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# # init SQLAlchemy so we can use it later in our models
# db = SQLAlchemy()
#
# def create_app():
#     app = Flask(__name__)
#
#     app.config['SECRET_KEY'] = 'secret-key-goes-here'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
#
#     db.init_app(app)
#
#     # blueprint for auth routes in our app
#     from .auth import auth as auth_blueprint
#     app.register_blueprint(auth_blueprint)
#
#     # blueprint for non-auth parts of app
#     from .main import main as main_blueprint
#     app.register_blueprint(main_blueprint)
#
#     return app
#
# ###
# project/main.py
# from flask import Blueprint
# from . import db
#
# main = Blueprint('main', __name__)
#
# @main.route('/')
# def index():
#     return 'Index'
#
# @main.route('/profile')
# def profile():
#     return 'Profile'
#
# ###
# from flask import Blueprint
# from . import db
#
# auth = Blueprint('auth', __name__)
#
# @auth.route('/login')
# def login():
#     return 'Login'
#
# @auth.route('/signup')
# def signup():
#     return 'Signup'
#
# @auth.route('/logout')
# def logout():
#     return 'Logout'
#
# ###
# export FLASK_APP=project
# export FLASK_DEBUG=1
#
# ###
# flask run