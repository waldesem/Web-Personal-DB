from datetime import datetime
from functools import wraps

import bcrypt
from flask import abort
from flask_jwt_extended import JWTManager, current_user, \
    create_access_token, create_refresh_token, get_jwt, jwt_required, get_jwt_identity

from . import bp
from ..models.model import TokenBlocklist, Report, User, db
from ..models.schema import LoginSchema, UserSchema
from ..models.classify import Roles

jwt = JWTManager()


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    """
    Check if a JWT token is revoked.
    Parameters:
        jwt_header (str): The JWT header containing information about the token.
        jwt_payload (dict): The JWT payload containing information about the token.
    Returns:
        bool: True if the token is revoked, False otherwise.
    """
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None


@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    A function that acts as a user identity loader for the JWT framework.
    Parameters:
        user (Any): The user object to be used for user identity.
    Returns:
        Any: The user object.
    """
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Look up a user based on JWT data.
    Parameters:
        _jwt_header (dict): The JWT header.
        jwt_data (dict): The JWT data.
    Returns:
        User: The user found based on the JWT data, or None if not found.
    """
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()


@bp.get('/auth')
@jwt_required()
@bp.doc(hide=True)
def auth(): 
    """
    A function that handles the authentication process.
    Returns:
        dict: A dictionary with the access status.
            - 'access': 'Authorized' if the user is authorized, 'Denied' otherwise.
    """
    user = db.session.query(User).filter_by(username=current_user.username).one_or_none()
    if user and not user.has_blocked():
        user.last_login = datetime.now()
        db.session.commit()
        schema = UserSchema()
        usr = schema.dump(user)
        return {'access': 'Authorized'} | usr
    return {'access': 'Denied'}


@bp.post('/login')
@bp.input(LoginSchema)
@bp.doc(hide=True)
def login(json_data):
    """
    Logs in a user and returns an access token and refresh token if successful.
    Parameters:
        response (dict): The response from the login form containing the username and password.   
    Returns:
        dict: A dictionary containing the access status, access token, and refresh token.
            - 'access': The access status, which can be 'Authorized', 'Overdue', or 'Denied'.
            - 'access_token': The access token if the login is successful, otherwise None.
            - 'refresh_token': The refresh token if the login is successful, otherwise None.
    """
    user = db.session.query(User).filter_by(username=json_data['username']).one_or_none()
    if user and not user.blocked and not user.has_role(Roles.api.value):
        if bcrypt.checkpw(json_data['password'].encode('utf-8'), user.password):
            delta_change = datetime.now() - user.pswd_create
            if user.pswd_change and delta_change.days < 365:
                user.last_login = datetime.now()
                user.attempt = 0
                db.session.commit()
                schema = UserSchema()
                usr = schema.dump(user)
                return {'access': 'Authorized', 
                        'access_token': create_access_token(identity=user.username), 
                        'refresh_token': create_refresh_token(identity=user.username)} | usr
            return {"access": "Overdue"}
        else:
            if user.attempt < 4:
                user.attempt = user.attempt+1
            else:
                user.blocked = True
                admins = db.session.query(User).filter(User.role.in_(['admin'])).all()
                for admin in admins:
                    db.session.add(Report(message=f'Заблокирован пользователь {user["username"]}. \
                                           Превышение попыток входа', 
                                            user_id=admin.id))
            db.session.commit()
    return {"access": "Denied"}


@bp.post('/password')
@bp.input(LoginSchema)
@bp.doc(hide=True)
def change_password(json_data):
    """
    Change the password for a user.
    Args:
        response (dict): The response object containing the username, current password, 
                         and new password.
    Returns:
        dict: A dictionary with the access status and an access token (set to None).
    """
    user = db.session.query(User).filter_by(username=json_data['username']).one_or_none()
    if user:
        if bcrypt.checkpw(json_data['password'].encode('utf-8'), user.password):
            setattr(user, 'password', bcrypt.hashpw(json_data['new_pswd'].encode('utf-8'), 
                                                    bcrypt.gensalt()))
            setattr(user, "pswd_change", datetime.now())
            db.session.commit()
            return {"access": "Success"}
    return {"access": "Denied"}


@bp.delete('/logout')
@bp.doc(hide=True)
@jwt_required(verify_type=False)
def logout():
    """
    Logout the user and invalidate the access token.
    Returns:
    A dictionary with a single key-value pair:
    - `access`: A string representing the access level, which is set to 'Default' after successful logout.
    """
    jti = get_jwt()["jti"]
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return {'access': 'Default'}


@bp.post("/refresh")
@bp.doc(hide=True)
@jwt_required(refresh=True)
def refresh():
    """
    Generates a new access token for the current user.
    :return: A dictionary containing the new access token.
    :rtype: dict
    """
    access_token = create_access_token(identity=get_jwt_identity())
    return {'access_token': access_token}


def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = db.session.query(User).filter_by(username=get_jwt_identity()).one_or_none()
            if user is not None and any(user.has_role(role) for role in roles):
                return func(*args, **kwargs)
            else:
                abort(404)
        return wrapper
    return decorator


def group_required(*groups):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user = db.session.query(User).filter_by(username=get_jwt_identity()).one_or_none()
            if user is not None and any(user.has_group(group) for group in groups):
                return func(*args, **kwargs)
            else:
                abort(404)
        return wrapper
    return decorator