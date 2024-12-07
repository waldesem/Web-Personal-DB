import re

from flask import Blueprint, current_app, jsonify, request
from sqlalchemy import desc, func, select
from werkzeug.security import generate_password_hash

from ..depends.depend import (
    current_user,
    get_current_user,
    get_payload,
    roles_required,
    validate,
)
from ..model.classes import Regions, Roles
from ..model.models import User, UserActions
from ..model.tables import  Users, db_session


bp = Blueprint("users", __name__, url_prefix="/users")


@bp.get("/")
@roles_required(Roles.admin.value)
def get_users():
    """
    Retrieves a list of users from the database based on the provided search criteria.

    Parameters:
        item (str): The table name from which to retrieve the users.

    Returns:
        tuple: A tuple containing the JSON-encoded list of users and the HTTP status code.
    """
    search_data = request.args.get("search")
    stmt = select(Users)
    if search_data and len(search_data) > 2:
        if re.match(r"^[a-zA-z_]+", search_data):
            stmt = stmt.filter(func.lower(Users.username) == search_data.lower())
        else:
            stmt = stmt.filter(func.lower(Users.fullname) == search_data.lower())
    users = db_session.execute(stmt.order_by(desc(Users.id))).scalars()
    return jsonify([user.to_dict() for user in users]), 200


@bp.post("/")
@validate()
@roles_required(Roles.admin.value)
def post_user(json_data: User):
    """
    Handles the POST request to create a user in the database.

    This function is a route handler for the '/users' endpoint with the HTTP method POST.
    It requires a valid token for authentication.

    Returns:
        - If the user already exists returns an empty response with status code 200.
        - Else generates a hashed password using the default password.
        Returns an empty response with status code 201.
        - If an exception occurs during the execution of the function,
        returns an empty response with status code 200.
    """
    user = db_session.execute(
        select(Users).filter(
            func.lower(Users.username) == json_data.username.lower()
        )
    ).all()
    if not user:
        db_session.add(Users(
            fullname=json_data.fullname,
            username=json_data.username,
            email=json_data.email,
            role=Roles.guest.value,
            region=Regions.main.value,
            passhash=generate_password_hash(current_app.config["DEFAULT_PASSWORD"]),
        ))
        db_session.commit()
        return jsonify({"message": "success"}), 201
    return jsonify({"message": "error"}), 200


@bp.get("/<int:user_id>")
@validate()
@roles_required(Roles.admin.value)
def get_user_actions(user_id, query_data: UserActions):
    """
    Change a user's information in the database based on their user ID.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        The HTTP status code is 201.
    """
    if current_user.get("id") == user_id:
        return jsonify({"message": "error"}), 200
    user = db_session.get(Users, user_id)
    if user and query_data.item:
        if query_data.item == "drop":
            user.passhash = generate_password_hash(
                current_app.config["DEFAULT_PASSWORD"]
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
        get_payload.cache_clear()
    return "", 201
