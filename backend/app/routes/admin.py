import bcrypt
from apiflask import EmptySchema
from flask import abort
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select
from sqlalchemy_searchable import search

from config import Config
from . import bp
from .login import roles_required
from ..models.classes import Roles
from ..models.model import db, User, Role
from ..models.schema import (
    ActionSchema,
    SearchSchema,
    UserSchema,
)


@roles_required(Roles.admin.value)
@bp.doc(hide=True)
@bp.get("/users")
@bp.input(SearchSchema, location="query")
def get_users(query_data):
    """
    Endpoint to handle requests for getting users.
    """
    search_data = query_data.get("search")
    query = search(select(User), search_data if search_data else "").order_by(
        User.id.asc()
    )
    result = db.session.scalars(query).all()
    return UserSchema().dump(result, many=True), 200


class UserView(MethodView):

    decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

    @bp.input(ActionSchema, location="query")
    def get(self, user_id, query_data):
        """
        Retrieves a user based on the specified action and user ID.
        """
        action_data = query_data.get("action")
        if action_data != "view":
            user = db.session.get(User, user_id)
            match action_data:
                case "block":
                    if user.username != current_user.username:
                        user.blocked = not user.blocked
                case "drop":
                    user.password = bcrypt.hashpw(
                        Config.DEFAULT_PASSWORD.encode("utf-8"),
                        bcrypt.gensalt(),
                    )
                    user.attempt = 0
                    user.pswd_change = None
                case _:
                    return abort, 404
            db.session.commit()
        user = db.session.get(User, user_id)
        return UserSchema().dump(user), 200

    @bp.input(UserSchema)
    def post(self, json_data):
        """
        Creates a new user based on the provided JSON data.
        """
        if not User.get_user(json_data.get("username")):
            db.session.add(
                User(
                    fullname=json_data.get("fullname"),
                    username=json_data.get("username"),
                    email=json_data.get("email"),
                    password=bcrypt.hashpw(
                        Config.DEFAULT_PASSWORD.encode("utf-8"),
                        bcrypt.gensalt(),
                    ),
                )
            )
            db.session.commit()
            return {"message": "Created"}, 201
        return {"message": "Denied"}, 403

    @bp.input(UserSchema)
    def patch(self, user_id, json_data):
        """
        Patch a user's information.
        """
        user = db.session.get(User, user_id)
        if user:
            for key, value in json_data.items():
                setattr(user, key, value)
            db.session.commit()
            return {"message": "Changed"}, 201
        return {"message": "Denied"}, 403

    @bp.output(EmptySchema)
    def delete(self, user_id):
        """
        Delete a user by their ID.
        """
        user = db.session.get(User, user_id)
        if user and user.username != current_user.username:
            user.deleted = True
            db.session.commit()
            return "", 204
        return "", 403


user_view = UserView.as_view("user")
bp.add_url_rule("/user", view_func=user_view, methods=["POST"])
bp.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["DELETE", "GET", "PATCH"]
)


class RoleView(MethodView):
    """
    Get a user's role based on the value and user ID.
    """

    decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

    def get(self, value, user_id):
        user = db.session.get(User, user_id)
        role = db.session.get(Role, value)
        if user and role not in user.roles:
            user.roles.append(role)
            db.session.commit()
            return "", 201
        return "", 403

    def delete(self, value, user_id):
        """
        Deletes a role from a user.
        """
        user = db.session.get(User, user_id)
        role = db.session.get(Role, value)
        if (
            user
            and role
            and (
                user.username != current_user.username or role.role != Roles.admin.value
            )
        ):
            user.roles.remove(role)
            db.session.commit()
            return "", 201
        return "", 403


bp.add_url_rule("/role/<value>/<int:user_id>", view_func=RoleView.as_view("role"))
