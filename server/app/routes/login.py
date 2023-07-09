from datetime import datetime

import bcrypt
from flask import jsonify, request
from flask_jwt_extended import JWTManager, \
    create_access_token, get_jwt_identity, \
    jwt_required, unset_jwt_cookies, current_user

from . import bp
from ..models.model import User, UserSchema, db

jwt = JWTManager()


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()


@bp.get('/auth')
@bp.doc(hide=True)
@jwt_required()
def auth():
    """
    Returns the current user's username if the user is authenticated, otherwise returns "None".
    """
    # verify_jwt_in_request(optional=True)
    user = get_jwt_identity()
    if current_user.username == user:
        userlogin = db.session.query(User).filter_by(username=user).first()
        if userlogin and not userlogin.blocked:
            userlogin.last_login = datetime.now()
            db.session.commit()
            return {"user": "Authorized"}
        else:
            return {"user": "None"}  # if the user is not authenticated, return "None"
    else:
        return {"user": "None"}  # if the user is not authenticated, return "None"


@bp.post('/login')
@bp.doc(hide=True)
def login():
    """
    Logs in a user and returns their username if the credentials provided are correct.
    """
    # Get user data from the form
    user_form = request.get_json()
    username = user_form.get('username')
    password = user_form.get('password')
    # Query the database for a user with the provided credentials
    user = db.session.query(User).filter_by(username=username).one_or_none()
    # If a user with the provided credentials exists, log them in and return their username
    if user and not user.blocked:
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            
            delta_change = datetime.now() - user.pswd_create
            if user.pswd_change and delta_change.days < 365:
                access_token = create_access_token(identity=username)
                user.last_login = datetime.now()
                db.session.commit()
                return {'user': 'Authorized', 'access_token': access_token}
            else:
                return {"user": "Overdue"}
    return {"user": "None", 'access_token': "None"}


@bp.get('/logout')
@bp.doc(hide=True)
def logout():
    unset_jwt_cookies(jsonify({"user": "None"}))
    # Return a dictionary with a "user" key and a value of "None".
    return {"user": "None"}


@bp.post('/password')
@bp.doc(hide=True)
def change_password():
    # Get user data from the form
    user_form = request.get_json()
    username = user_form.get('username')
    password = user_form.get('password')
    new_pswd = user_form.get('new_pswd')
    conf_pswd = user_form.get('conf_pswd')

    if conf_pswd != new_pswd:
        return {"user": "Not_match"}

    # Query the database for a user with the provided credentials
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            setattr(user, 'password', bcrypt.hashpw(new_pswd.encode('utf-8'), bcrypt.gensalt()))
            setattr(user, "pswd_change", datetime.now())
            db.session.commit()
            return {"user": "Success"}
        else:
            return {"user": "Denied"}
    else:
        return {"user": "Denied"}
