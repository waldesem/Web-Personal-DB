import datetime

import bcrypt
from flask import request
from flask_login import login_user, logout_user, current_user
from apiflask.views import MethodView
from flask_login import LoginManager

from . import bp
from ..models.model import User, db

lm = LoginManager()
lm.login_view = 'route.login'  


class Login(MethodView):

    def get(self):
        """
        Returns the current user's username if the user is authenticated, otherwise returns "None".
        """
        if current_user.is_authenticated:  # check if the user is authenticated
            return {"user": current_user.username}
        else:
            return {"user": "None"}  # if the user is not authenticated, return "None"

    def post(self):
        """
        Logs in a user and returns their username if the credentials provided are correct.
        """
        # Get user data from the form
        user_form = request.form.to_dict()
        username = user_form.get('username')
        password = user_form.get('password')
        remember = bool(user_form.get('remember'))

        # Query the database for a user with the provided credentials
        user = db.session.query(User).filter_by(username=username).first()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password):
                delta_change = datetime.date.today()- user.pswd_create
                if user.pswd_change and delta_change.days < 365:
                    login_user(user, remember=remember)
                    return {"user": current_user.username}
                else:
                    return {"user": "Overdue"}
            else:
                return {"user": "None"}
        # Otherwise, return "None"
        else:
            return {"user": "None"}


bp.add_url_rule('/login', view_func=Login.as_view('login'))


@bp.get('/logout')
def logout():
    """
    Logs out the user from the system.

    Returns:
        dict: A dictionary with a "user" key, whose value is "None".
    """
    # Call the logout_user function to log out the user.
    logout_user()

    # Return a dictionary with a "user" key and a value of "None".
    return {"user": "None"}


@bp.post('/registration')
def registration():

    # Get user data from the form
    user_form = request.form.to_dict()
    fullname = user_form.get('fullname')
    username = user_form.get('username')

    # Query the database for a user with the provided credentials
    user = db.session.query(User).filter_by(username=username).first()

    if user:
        return {"response": "Error"}
    else:
        new_user = User(
            fullname=fullname,
            username=username, 
            
            pswd_create = datetime.date.today()
            )       
        db.session.add(new_user)
        db.session.commit()
        setattr(new_user, 'password', bcrypt.hashpw(username.encode('utf-8'), bcrypt.gensalt()))
        db.session.commit()
        return {"response": username}


@bp.post('/password')
def change_password():

    # Get user data from the form
    user_form = request.form.to_dict()
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
            setattr(user, "pswd_change", datetime.date.today())
            db.session.commit()
            return {"user": "Success"}
        else:
            return {"user": "Denied"}
    else:
        return {"user": "Denied"}
        