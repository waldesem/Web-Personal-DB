"""User routes."""

from typing import ClassVar

from flask import Blueprint, Response, current_app, jsonify
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash

from app.depends.depend import auth_required, current_user, get_current_user, validate
from app.model.classes import Regions, Roles
from app.model.models import User, UserActions
from app.model.tables import Users, db_session

bp = Blueprint("users", __name__)


@bp.get("/users")
@auth_required(Roles.admin.value)
def get_users() -> Response:
    """Retrieve a list of users from the database.

    Arguments:
       None.

    Returns:
        tuple: A tuple containing the JSON-encoded list of users.

    """
    columns = list(filter(lambda x: x != "passhash", Users.__table__.columns.keys()))
    stmt = select(*[getattr(Users, column) for column in columns])
    users = db_session.execute(stmt).all()
    return jsonify([user._asdict() for user in users]), 200


class UserView(MethodView):
    """User view class."""

    decorators: ClassVar = [auth_required(Roles.admin.value)]

    @validate
    def get(self, user_id: int, query_data: UserActions) -> Response:
        """Change a user's information in the database based on their user ID.

        Args:
            user_id (int): The ID of the user.
            query_data (UserActions): The user data to be updated in the database.

        Returns:
            The HTTP status code is 201.

        """
        user = db_session.get(Users, user_id)
        if not user or current_user.id == user.id:
            return jsonify({"message": "error"}), 200

        if query_data.item == "reset":
            user.passhash = generate_password_hash(
                current_app.config["DEFAULT_PASSWORD"],
            )
            user.attempt = 0
            user.blocked = False
            user.change_pswd = True
        elif query_data.item == "block":
            user.blocked = not user.blocked
        elif query_data.item == "delete":
            user.deleted = not user.deleted
        elif query_data.item in [reg.value for reg in Roles]:
            user.role = query_data.item
        elif query_data.item in [reg.value for reg in Regions]:
            user.region = query_data.item
        else:
            return jsonify({"message": "error"}), 200
        db_session.commit()
        get_current_user.cache_clear()
        return jsonify({"message": "success"}), 201

    @validate
    def post(self, json_data: User) -> Response:
        """Handle the POST request to create a user in the database.

        Arguments:
            json_data (User): The user data to be added to the database.

        Returns:
            - If the user already exists returns an empty response with status code 200.
            - Otherwise returns a response with status code 201.

        """
        user = db_session.execute(
            select(Users).filter(Users.username == json_data.username),
        ).all()
        if user:
            return jsonify({"message": "error"}), 200
        try:
            db_session.add(
                Users(
                    fullname=json_data.fullname,
                    username=json_data.username,
                    email=json_data.email,
                ),
            )
            db_session.commit()
            return jsonify({"message": "success"}), 201
        except SQLAlchemyError:
            current_app.logger.exception("Database error")
            db_session.rollback()
            return jsonify({"message": "error"}), 200


view_func = UserView.as_view("user")
bp.add_url_rule("/user", view_func=view_func, methods=["POST"])
bp.add_url_rule(
    "/user/<int:user_id>",
    view_func=view_func,
    methods=["GET"],
)
