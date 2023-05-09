from flask import request
from flask_login import login_user, logout_user, current_user
from apiflask.views import MethodView

from . import bp
from ..models.model import User, db


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
        user = db.session.query(User).filter_by(username=username, password=password).first()

        # If a user with the provided credentials exists, log them in and return their username
        if user:
            login_user(user, remember=remember)
            return {"user": current_user.username}
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
