import bcrypt
from apiflask import EmptySchema
from flask import abort
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select
from sqlalchemy_searchable import search

from config import Config
from . import bp_admin
from ... import db
from ..login.login import group_required
from ...models.classes import Roles, Groups
from ...models.model import User, Role, Group
from ...models.schema import (
    ActionSchema,
    SearchSchema,
    AdminUserSchema,
    UserSchema,
    models_schemas,
)


class UsersView(MethodView):

    decorators = [group_required(Groups.admins.value), bp_admin.doc(hide=True)]

    @bp_admin.input(SearchSchema, location="query")
    def get(self, query_data):
        """
        Endpoint to handle requests for getting users.
        """
        search_data = query_data.get("search")
        query = (
            search(select(User), search_data if search_data else "")
            .order_by(User.id.asc())
        )
        result = db.session.scalars(query).all()
        return UserSchema().dump(result, many=True), 200


bp_admin.add_url_rule("/users", view_func=UsersView.as_view("users"))


class UserView(MethodView):

    decorators = [group_required(Groups.admins.value), bp_admin.doc(hide=True)]

    @bp_admin.input(ActionSchema, location="query")
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
                case "restore":
                    user.deleted = False
                case _:
                    return abort, 404
            db.session.commit()
        user = db.session.get(User, user_id)
        return UserSchema().dump(user), 200

    @bp_admin.input(AdminUserSchema)
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

    @bp_admin.input(AdminUserSchema)
    def patch(self, json_data):
        """
        Patch a user's information.
        """
        user = User.get_user(json_data.get("username"))
        if user:
            user.fullname = json_data.get("fullname")
            user.email = json_data.get("email")
            db.session.commit()
            return {"message": "Changed"}, 201
        return {"message": "Denied"}, 403

    @bp_admin.output(EmptySchema)
    def delete(self, user_id):
        """
        Delete a user by their ID.
        """
        user = db.session.get(User, user_id)
        if user and user.username != current_user.username:
            user.deleted = True
            db.session.commit()
            return {"message": "Deleted"}, 204
        return {"message": "Denied"}, 403


user_view = UserView.as_view("user")
bp_admin.add_url_rule("/user", view_func=user_view, methods=["PATCH", "POST"])
bp_admin.add_url_rule("/user/<int:user_id>", view_func=user_view, methods=["DELETE", "GET"])


class GroupView(MethodView):

    decorators = [group_required(Groups.admins.value), bp_admin.doc(hide=True)]

    def get(self, value, user_id):
        """
        Retrieves a user's group from the database and adds it to the user's
        list of groups if it does not already exist.
        """
        user = db.session.get(User, user_id)
        group = db.session.get(Group, value)
        if user and group not in user.groups:
            user.groups.append(group)
            db.session.commit()
            return {"message": "Added"}, 200
        return {"message": "Denied"}, 403

    @bp_admin.output(EmptySchema)
    def delete(self, value, user_id):
        """
        Deletes a group from a user's list of groups.
        """
        user = db.session.get(User, user_id)
        group = db.session.get(Group, value)
        if (
            user
            and group
            and (user.username != current_user.username
            or group.group != Groups.admins.value)
        ):
            user.groups.remove(group)
            db.session.commit()
            return {"message": "Removed"}, 200
        return {"message": "Denied"}, 403


bp_admin.add_url_rule("/group/<value>/<int:user_id>", view_func=GroupView.as_view("group"))


class RoleView(MethodView):
    """
    Get a user's role based on the value and user ID.
    """

    decorators = [group_required(Groups.admins.value), bp_admin.doc(hide=True)]

    def get(self, value, user_id):
        user = db.session.get(User, user_id)
        role = db.session.get(Role, value)
        if user and role not in user.roles:
            user.roles.append(role)
            db.session.commit()
            return {"message": "Added"}, 200
        return {"message": "Denied"}, 403

    def delete(self, value, user_id):
        """
        Deletes a role from a user.
        """
        user = db.session.get(User, user_id)
        role = db.session.get(Role, value)
        if (
            user
            and role
            and (user.username != current_user.username  
            or role.role != Roles.admin.value)
        ):
            user.roles.remove(role)
            db.session.commit()
            return {"message": "Removed"}, 200
        return {"message": "Denied"}, 403


bp_admin.add_url_rule("/role/<value>/<int:user_id>", view_func=RoleView.as_view("role"))


class TableView(MethodView):

    decorators = [group_required(Groups.admins.value), bp_admin.doc(hide=True)]

    @bp_admin.input(SearchSchema, location="query")
    def get(self, item, num, query_data):
        model = models_schemas[item][0]
        schema = models_schemas[item][1]

        query = select(model).order_by(model.id.desc())
        search_data = query_data.get("search")
        if search_data:
            query = query.filter_by(id=search_data)
        result = db.paginate(
            query,
            page=num,
            per_page=Config.PAGINATION,
            error_out=False,
        )
        return [
            schema.dump(result, many=True),
            {"has_next": result.has_next, "has_prev": result.has_prev},
        ], 200

    def delete(self, item, num):
        if not item == "user":
            model = models_schemas[item][0]
            row = db.session.get(model, num)
            db.session.delete(row)
            db.session.commit()
            return {"message": "Deleted"}, 204
        return {"message": "Denied"}, 403


bp_admin.add_url_rule("/table/<item>/<int:num>", view_func=TableView.as_view("table"))
