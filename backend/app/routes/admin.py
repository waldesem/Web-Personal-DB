import bcrypt

from flask_jwt_extended import current_user

from . import bp
from .login import roles_required
from ..models.model import  User, Role, Group, db
from ..models.schema import  UserSchema
from ..models.classify import Roles


@bp.get('/admin')
@roles_required(Roles.admin.value)
@bp.doc(hide=True)
def get_admin():
    """
    Retrieves the admin status of the current user.
    Returns:
        dict: A dictionary containing the admin status of the user.
    """
    user = db.session.query(User).filter_by(username=current_user.username).one_or_none()
    return {"admin": user.has_role(Roles.admin.value)}


@bp.get('/users')
@roles_required(Roles.admin.value)
@bp.doc(hide=True)
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
@roles_required(Roles.admin.value)
@bp.output(UserSchema)
@bp.doc(hide=True)
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
@roles_required(Roles.admin.value)
@bp.input(UserSchema)
@bp.doc(hide=True)
def add_user_info(flag, json_data):
    """
    Add user information to the database.
    Args:
        flag (str): A flag indicating the type of user information to add. 
    Returns:
        dict: A dictionary containing the response for the given flag. If the flag is 'edit', the dictionary will contain the updated user information. 
        If the flag is anything other than 'edit', the dictionary will contain the value 'none'.
    """
    # response = request.get_json()
    user = db.session.query(User).filter_by(username=json_data['username']).one_or_none()
    if not user:
        new_user = User(fullname=json_data['fullname'],
                        username=json_data['username'],
                        region_id = json_data['region_id'],
                        email = json_data['email'],
                        password=bcrypt.hashpw(json_data['username'].encode('utf-8'), bcrypt.gensalt()))
        db.session.add(new_user)
        db.session.commit()
        return {'user': flag}

    elif flag == "edit":
        for k, v in json_data.items():
            setattr(user, k, v)
        db.session.commit()
        return {'user': flag}

    else:
        return {'user': 'none'}


@bp.get('/user/<flag>/<int:user_id>')
@roles_required(Roles.admin.value)
@bp.doc(hide=True)
def user_state(user_id, flag):
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
            user.blocked = not user.blocked
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


@bp.get('/admin/<flag>/<action>/<value>/<int:user_id>')
@roles_required(Roles.admin.value)
@bp.doc(hide=True)
def action_role_group(flag, action, value, user_id):

    user = db.session.query(User).get(user_id)
    item = db.session.query(Role).filter_by(role=value).first() \
        if flag == 'role' else db.session.query(Group).filter_by(group=value).first() 
    
    if item:
        response = user.has_role(value) if flag == 'role' else user.has_group(value)
        
        if action == 'add' and not response:
            user.roles.append(item) if flag == 'role' else user.groups.append(item)
            db.session.commit()
            return {'result': 'Success'}
        
        elif action == 'remove':
            if user.username == current_user.username and value == 'admin':
                return {'result': 'Denied'}
            else:
                user.roles.remove(item) if flag == 'role' else user.groups.remove(item)
                db.session.commit()
                return {'result': 'Success'}
    
    return {'result': 'Failed'}

