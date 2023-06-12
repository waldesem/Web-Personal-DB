import datetime

import bcrypt
from flask import jsonify, request
from apiflask.views import MethodView
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies, verify_jwt_in_request

from . import bp
from ..models.model import User, db

jwt = JWTManager()


class Login(MethodView):

    @jwt_required()
    def get(self):
        """
        Returns the current user's username if the user is authenticated, otherwise returns "None".
        """
        #verify_jwt_in_request(optional=True)        
        current_user = get_jwt_identity()

        if current_user:
            return {"user": "Authorized"}
        else:
            return {"user": "None"}  # if the user is not authenticated, return "None"
    
    def post(self):
        """
        Logs in a user and returns their username if the credentials provided are correct.
        """
        verify_jwt_in_request(optional=True)        
        # Get user data from the form
        user_form = request.form.to_dict()
        username = user_form.get('username')
        password = user_form.get('password')
        remember = bool(user_form.get('remember'))
        # Query the database for a user with the provided credentials
        user = db.session.query(User).filter_by(username=username, password=password).first()

        # If a user with the provided credentials exists, log them in and return their username
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password):
                delta_change = datetime.date.today()- user.pswd_create
                if user.pswd_change and delta_change.days < 365:
                    access_token = create_access_token(identity=username, remember=remember)
                    return {'user': 'Authorized', 'access_token': access_token}
                else:
                    return {"user": "Overdue"}
            else:
                return {"user": "None", 'access_token': "None"}
        # Otherwise, return "None"
        else:
            return {"user": "None", 'access_token': "None"}


bp.add_url_rule('/login', view_func=Login.as_view('login'))


@jwt_required()
@bp.get('/logout')
def logout():
    unset_jwt_cookies(jsonify({"user": "None"}))
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
        