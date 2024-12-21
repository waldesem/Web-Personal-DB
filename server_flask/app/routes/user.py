"""User routes."""

import re
from typing import ClassVar

from flask import Blueprint, Response, current_app, jsonify
from flask.views import MethodView
from sqlalchemy import desc, func, select
from werkzeug.security import generate_password_hash

from app.depends.depend import current_user, get_current_user, roles_required, validate
from app.model.classes import Regions, Roles
from app.model.models import Search, User, UserActions
from app.model.tables import Users, db_session

bp = Blueprint("users", __name__)


class UserView(MethodView):
    """User view class."""

    decorators: ClassVar = [roles_required(Roles.admin.value)]

    @validate()
    def get(self, query_data: Search) -> Response:
        """Retrieve a list of users from the database.

        Arguments:
            item (str): The table name from which to retrieve the users.
            query_data (Search): The search query containing the search string.

        Returns:
            tuple: A tuple containing the JSON-encoded list of users.

        """
        stmt = select(Users)
        if query_data.search and len(query_data.search) > 2:  # noqa: PLR2004
            if re.match(r"^[a-zA-z_]+", query_data.search):
                stmt = stmt.filter(
                    func.lower(Users.username) == query_data.search.lower(),
                )
            else:
                stmt = stmt.filter(
                    func.lower(Users.fullname) == query_data.search.lower(),
                )
        users = db_session.execute(stmt.order_by(desc(Users.id))).scalars()
        return jsonify([user.to_dict() for user in users]), 200

    @validate()
    def post(self, json_data: User) -> Response:
        """Handle the POST request to create a user in the database.

        Arguments:
            json_data (User): The user data to be added to the database.

        Returns:
            - If the user already exists returns an empty response with status code 200.
            - Else generates a hashed password using the default password.
            Returns an empty response with status code 201.
            - If an exception occurs during the execution of the function,
            returns an empty response with status code 200.

        """
        user = db_session.execute(
            select(Users).filter(
                func.lower(Users.username) == json_data.username.lower(),
            ),
        ).all()
        if not user:
            db_session.add(
                Users(
                    fullname=json_data.fullname,
                    username=json_data.username,
                    email=json_data.email,
                ),
            )
            db_session.commit()
            return jsonify({"message": "success"}), 201
        return jsonify({"message": "error"}), 200


bp.add_url_rule("/users", view_func=UserView.as_view("users"))


@bp.get("/user/<int:user_id>")
@validate()
@roles_required(Roles.admin.value)
def get_user_actions(user_id: int, query_data: UserActions) -> Response:
    """Change a user's information in the database based on their user ID.

    Args:
        user_id (int): The ID of the user.
        query_data (UserActions): The user data to be updated in the database.

    Returns:
        The HTTP status code is 201.

    """
    if current_user.id == user_id:
        return jsonify({"message": "error"}), 200
    user = db_session.get(Users, user_id)
    if user and query_data.item:
        if query_data.item == "drop":
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
        db_session.commit()
        get_current_user.cache_clear()
    return "", 201
