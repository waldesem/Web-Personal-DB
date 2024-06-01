from datetime import datetime

from flask import abort, jsonify, request
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash, generate_password_hash

from . import bp
from ..utils.dependencies import Token, create_token, jwt_required
from ..models.model import engine, User


class AuthView(MethodView):
    """Login view"""

    decorators = [jwt_required()]

    def get(self):
        """
        Retrieves the current authenticated user from the database.
        """
        if (
            Token.current_user
            and not Token.current_user.blocked
            and not Token.current_user.deleted
        ):
            with Session(engine) as session:
                Token.current_user.last_login = datetime.now()
                user_dict = Token.current_user.__dict__
                user_dict.update(
                    {"roles": [role.role for role in Token.current_user.roles]}
                )
                del user_dict["_sa_instance_state"], user_dict["password"]
                session.commit()
                return jsonify(user_dict)
        return abort(404)


bp.add_url_rule("/auth", view_func=AuthView.as_view("auth"))


class LoginView(MethodView):
    """Login view"""

    def post(self):
        """
        Post method for the given API endpoint.
        """
        json_data = request.get_json()
        with Session(engine) as session:
            user = User.get_user(json_data["username"])
            if user and not user.blocked and not user.deleted:
                if check_password_hash(user.password, json_data["password"]):
                    delta_change = datetime.now() - user.pswd_create
                    if user.pswd_change and delta_change.days < 365:
                        user.last_login = datetime.now()
                        user.attempt = 0
                        session.commit()
                        return jsonify({
                            "message": "Authenticated",
                            "user_token": create_token(str(user.id)),
                        }), 201
                    return jsonify({"message": "Overdue"}), 201
                else:
                    if user.attempt < 9:
                        user.attempt += 1
                    else:
                        user.blocked = True
                    session.commit()

            return jsonify({"message": "Denied"}), 201

    def patch(self):
        """
        Patch method for updating user password.
        """
        json_data = request.get_json()
        with Session(engine) as session:
            user = session.execute(
                select(User).filter_by(username=json_data["username"])
            ).scalar_one_or_none()
            if (
                user
                and not user.blocked
                and not user.deleted
                and check_password_hash(user.password, json_data["password"])
            ):
                user.password = generate_password_hash(
                    json_data["new_pswd"],
                    method="scrypt",
                    salt_length=16,
                )
                user.pswd_change = datetime.now()
                session.commit()
                return jsonify({"message": "Changed"})
        return jsonify({"message": "Denied"})


bp.add_url_rule("/login", view_func=LoginView.as_view("login"))
