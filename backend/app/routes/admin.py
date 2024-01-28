import bcrypt
from apiflask import EmptySchema
from flask import current_app
from flask_jwt_extended import get_jwt_identity
from flask.views import MethodView
from sqlalchemy import select

from . import bp
from .. import db
from .login import roles_required, group_required
from ..models.classes import Roles, Groups
from ..models.model import User, Role, Group
from ..models.schema import SearchSchema, UserSchema, models_schemas


class UsersView(MethodView):
    decorators = [
        group_required(Groups.admins.value),
        bp.input(UserSchema),
        bp.doc(hide=True),
    ]

    def post(self, json_data):
        """
        Endpoint to handle POST requests for creating new users.
        """
        query = (
            db.session.execute(
                select(User)
                .order_by(User.id.desc())
                .filter_by(deleted=False)
                .search("%{}%".format(json_data["fullname"]))
            )
            .scalars()
            .all()
        )
        return UserSchema().dump(query, many=True)


bp.add_url_rule("/users", view_func=UsersView.as_view("users"))


class UserView(MethodView):
    decorators = [group_required(Groups.admins.value), bp.doc(hide=True)]

    def get(self, action, user_id):
        """
        Retrieves a user based on the specified action and user ID.
        """
        user = db.session.get(User, user_id)
        match action:
            case "view":
                return UserSchema().dump(user)
            case "block":
                if user.username != get_jwt_identity():
                    user.blocked = not user.blocked
            case "drop":
                new_pswd = bcrypt.hashpw(
                    current_app.config["DEFAULT_PASSWORD"].encode("utf-8"),
                    bcrypt.gensalt(),
                )
                user.password = new_pswd
                user.pswd_change = None
        db.session.commit()
        return {"message": action}, 200

    @bp.input(UserSchema)
    def post(self, json_data):
        """
        Creates a new user based on the provided JSON data.
        """
        if not User.get_user(json_data["username"]):
            new_pswd = bcrypt.hashpw(
                current_app.config["DEFAULT_PASSWORD"].encode("utf-8"), bcrypt.gensalt()
            )
            db.session.add(
                User(
                    fullname=json_data["fullname"],
                    username=json_data["username"],
                    email=json_data["email"],
                    password=new_pswd,
                )
            )
            db.session.commit()
            return {"message": "Created"}, 201
        return {"message": "Denied"}, 403

    @bp.input(UserSchema)
    def patch(self, json_data):
        """
        Patch a user's information.
        """
        user = db.session.get(User, json_data["id"])
        if user:
            user.fullname = json_data["fullname"]
            user.username = json_data["username"]
            user.email = json_data["email"]
            db.session.commit()
            return {"message": "Changed"}, 200
        return {"message": "Denied"}, 403

    @bp.output(EmptySchema)
    def delete(self, user_id):
        """
        Delete a user by their ID.
        """
        user = db.session.get(User, user_id)
        if user.username != get_jwt_identity():
            user.deleted = True
            db.session.commit()
        return {"message": "Deleted"}, 204


user_view = UserView.as_view("user")
bp.add_url_rule("/user", view_func=user_view, methods=["PATCH", "POST"])
bp.add_url_rule("/user/<int:user_id>", view_func=user_view, methods=["DELETE"])
bp.add_url_rule("/user/<action>/<int:user_id>", view_func=user_view, methods=["GET"])


class GroupView(MethodView):
    decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

    def get(self, value, user_id):
        """
        Retrieves a user's group from the database and adds it to the user's
        list of groups if it does not already exist.
        """
        user = db.session.get(User, user_id)
        if value not in user.groups:
            user.groups.append(db.session.get(Group, value))
            db.session.commit()
        return {"message": "Added"}, 200

    @bp.output(EmptySchema)
    def delete(self, value, user_id):
        """
        Deletes a group from a user's list of groups.
        """
        user = db.session.get(User, user_id)
        group = db.session.get(Group, value)
        if user.username != get_jwt_identity() and value != Roles.admin.value:
            user.groups.remove(group)
            db.session.commit()
        return {"message": "Removed"}, 200


bp.add_url_rule("/group/<value>/<int:user_id>", view_func=GroupView.as_view("group"))


class RoleView(MethodView):
    """
    Get a user's role based on the value and user ID.
    """

    decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

    def get(self, value, user_id):
        user = db.session.get(User, user_id)
        if value not in user.roles:
            user.roles.append(db.session.get(Role, value))
            db.session.commit()
        return {"message": "Added"}, 200

    def delete(self, value, user_id):
        """
        Deletes a role from a user.
        """
        user = db.session.get(User, user_id)
        role = db.session.get(Role, value)
        if user.username != get_jwt_identity() and value != Roles.admin.value:
            user.roles.remove(role)
            db.session.commit()
        return {"message": "Removed"}, 200


bp.add_url_rule("/role/<value>/<int:user_id>", view_func=RoleView.as_view("role"))


class TableView(MethodView):
    decorators = [group_required(Groups.admins.value), bp.doc(hide=True)]

    @bp.input(SearchSchema)
    def post(self, item, page, json_data):
        model = models_schemas[item][0]
        schema = models_schemas[item][1]
        query = select(model).order_by(model.id.desc())
        if item in ["user", "role", "group", "report", "resume", "connect"]:
            query = (
                query.filter_by(id=json_data["search"])
                if json_data["search"]
                else query
            )
        else:
            query = (
                query.filter_by(person_id=json_data["search"])
                if json_data["search"]
                else query
            )
        result = db.paginate(query, page=page, per_page=16, error_out=False)
        return [
            schema.dump(result, many=True),
            {"has_next": result.has_next, "has_prev": result.has_prev},
        ], 200

    def delete(self, item, item_id, page):
        model = models_schemas[item][0]
        row = db.session.get(model, item_id)
        if not item == "user":
            db.session.delete(row)
            db.session.commit()
        return {"message": "Deleted"}, 204


table_view = TableView.as_view("table")
bp.add_url_rule("/table/<item>/<int:page>", view_func=table_view, methods=["POST"])
bp.add_url_rule("/table/<item>/<int:item_id>", view_func=table_view, methods=["DELETE"])
