from functools import wraps
import bcrypt

from flask import request, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user

from . import bp
from ..models.model import  User, Region, db
from ..models.schema import  UserSchema
from ..models.classify import Role


def admin_required(func):
    """
    Decorator that checks if the user making the request is an admin. 
    If the user is an admin, the function is executed. Otherwise, a 404 error is returned.
    Parameters:
        func (function): The function to be decorated.
    Returns:
        function: The wrapped function.
    """
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs):
        admin = db.session.query(User).filter_by(username=get_jwt_identity()).one_or_none()
        if admin.has_role(Role.admin.value):
            return func(*args, **kwargs)
        else:
            abort(404)
    return wrapper


@bp.get('/admin')
@bp.doc(hide=True)
@jwt_required()
def get_admin():
    """
    Retrieves the admin status of the current user.
    Returns:
        dict: A dictionary containing the admin status of the user.
    """
    user = db.session.query(User).filter_by(username=current_user.username).one_or_none()
    return {"admin": user.has_role(Role.admin.value)}


@bp.get('/users')
@bp.doc(hide=True)
@admin_required
def get_users():
    """
    Retrieve all users from the database.
    Returns:
        list: A list of user data.
    """
    query = db.session.query(User).order_by(User.id.desc()).all()
    user_schema = UserSchema()
    datas = user_schema.dump(query, many=True)
    return datas


@bp.get('/user/<int:user_id>')
@bp.output(UserSchema)
@bp.doc(hide=True)
@admin_required
def get_user(user_id):
    """
    Get a user by their ID.
    Parameters:
        user_id (int): The ID of the user.
    Returns:
        User: The user object corresponding to the given ID.
    """
    return db.session.query(User).get(user_id)


@bp.post('/user/<flag>')
@bp.doc(hide=True)
@admin_required
def add_user_info(flag):
    """
    Add user information to the database.
    Args:
        flag (str): A flag indicating the type of user information to add. 
    Returns:
        dict: A dictionary containing the response for the given flag. If the flag is 'edit', the dictionary will contain the updated user information. If the flag is anything other than 'edit', the dictionary will contain the value 'none'.
    """
    response = request.get_json()
    user = db.session.query(User).filter_by(username=response['username']).one_or_none()
    if not user:
        new_user = User(fullname=response['fullname'],
                        username=response['username'],
                        region_id = response['region_id'],
                        email = response['email'],
                        password=bcrypt.hashpw(response['username'].encode('utf-8'), bcrypt.gensalt()),
                        role=response['role'])
        db.session.add(new_user)
        db.session.commit()
        return {'user': flag}

    elif flag == "edit":
        for k, v in response.items():
            setattr(user, k, v)
        db.session.commit()
        return {'user': flag}

    else:
        return {'user': 'none'}


@bp.get('/user/<int:user_id>/<flag>')
@bp.doc(hide=True)
@admin_required
def edit_user_info(user_id, flag):
    """
    Edit user information.
    Parameters:
        user_id (int): The ID of the user.
        flag (str): The flag indicating the action to be performed.
    Returns:
        dict: A dictionary containing the result of the operation. If the flag is 'block', it returns {'user': str}.
        If the flag is 'drop', it returns {'user': str}. Otherwise, it returns {'user': str}.
    """
    user = db.session.query(User).get(user_id)
    if user.username != current_user.username:
        if flag == 'block':
            setattr(user, 'blocked', False) if user.blocked else setattr(user, 'blocked', True)
            db.session.commit()
            return {'user': str(user.blocked)}
        if flag == 'drop':
            setattr(user, 'password', bcrypt.hashpw(user.username.encode('utf-8'), bcrypt.gensalt()))
            setattr(user, 'pswd_change', None)
            db.session.commit()
            return {'user': flag}
        else:
            db.session.delete(user)
            db.session.commit()
            return {'user': flag}
    return {'user': 'None'}

    
@bp.post('/region/add')
@bp.doc(hide=True)
@admin_required
def add_location():
    """
    Add a new location to the region.
    This function takes no parameters.
    Returns:
        dict: A dictionary containing the location status. If the location already exists, the value is False. Otherwise, the value is True.
    """
    response = request.get_json()
    location = db.session.query(Region).filter_by(region=response['region']).one_or_none()
    if not location:
        new_location = Region(region=response['region'])
        db.session.add(new_location)
        db.session.commit()
    return {'location': bool(location)}


@bp.get('/region/delete/<int:loc_id>')
@bp.doc(hide=True)
@admin_required
def del_location(loc_id):
    """
    Deletes a location from the database.
    Parameters:
        loc_id (int): The ID of the location to be deleted.
    Returns:
        dict: A dictionary containing the name of the deleted location.
    """
    location = db.session.query(Region).filter_by(id=loc_id).one_or_none()
    db.session.delete(location)
    db.session.commit()
    return {'location': location.region}
