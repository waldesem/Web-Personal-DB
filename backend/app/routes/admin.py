import bcrypt
from apiflask import EmptySchema
from flask import request, current_app
from flask_jwt_extended import get_jwt_identity
from flask.views import MethodView
from sqlalchemy import select

from . import bp
from .. import db
from .login import roles_required, group_required
from ..models.classes import Roles, Groups
from ..models.model import User, Role, Group
from ..models.schema import UserSchema, models_schemas


class UsersView(MethodView):
    decorators = [group_required(Groups.admins.value), bp.doc(hide=True)]

    def get(self):
        """
        Endpoint to handle requests for getting users.
        """
        search_data = request.args("search")
        query = (
            db.session.execute(
                select(User)
                .order_by(User.id.desc())
                .filter_by(deleted=False)
                .search("%{}%".format(search_data))
            )
            .scalars()
            .all()
        )
        return UserSchema().dump(query, many=True), 200


bp.add_url_rule("/users", view_func=UsersView.as_view("users"))


class UserView(MethodView):
    decorators = [group_required(Groups.admins.value), bp.doc(hide=True)]

    def get(self, user_id):
        """
        Retrieves a user based on the specified action and user ID.
        """
        action_data = request.args.get("action")
        user = db.session.get(User, user_id)
        if user and action_data:
            match action_data:
                case "view":
                    return UserSchema().dump(user), 200
                case "block":
                    if user.username != get_jwt_identity():
                        user.blocked = not user.blocked
                case "drop":
                    user.password = bcrypt.hashpw(
                        current_app.config["DEFAULT_PASSWORD"].encode("utf-8"),
                        bcrypt.gensalt(),
                    )
                    user.pswd_change = None
            db.session.commit()
            return {"message": action_data}, 200
        return {"message": "Denied"}, 403

    @bp.input(UserSchema)
    def post(self, json_data):
        """
        Creates a new user based on the provided JSON data.
        """
        if not User.get_user(json_data["username"]):
            db.session.add(
                User(
                    fullname=json_data["fullname"],
                    username=json_data["username"],
                    email=json_data["email"],
                    password=bcrypt.hashpw(
                        current_app.config["DEFAULT_PASSWORD"].encode("utf-8"),
                        bcrypt.gensalt(),
                    ),
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
            user.fullname = json_data.get("fullname")
            user.email = json_data.get("email")
            db.session.commit()
            return {"message": "Changed"}, 200
        return {"message": "Denied"}, 403

    @bp.output(EmptySchema)
    def delete(self, user_id):
        """
        Delete a user by their ID.
        """
        user = db.session.get(User, user_id)
        if user and user.username != get_jwt_identity():
            user.deleted = True
            db.session.commit()
            return {"message": "Deleted"}, 204
        return {"message": "Denied"}, 403


user_view = UserView.as_view("user")
bp.add_url_rule("/user", view_func=user_view, methods=["PATCH", "POST"])
bp.add_url_rule("/user/<int:user_id>", view_func=user_view, methods=["DELETE", "GET"])


class GroupView(MethodView):
    decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

    def get(self, value, user_id):
        """
        Retrieves a user's group from the database and adds it to the user's
        list of groups if it does not already exist.
        """
        user = db.session.get(User, user_id)
        if user and value not in user.groups:
            user.groups.append(Group.get_group(value))
            db.session.commit()
            return {"message": "Added"}, 200
        return {"message": "Denied"}, 403

    @bp.output(EmptySchema)
    def delete(self, value, user_id):
        """
        Deletes a group from a user's list of groups.
        """
        user = db.session.get(User, user_id)
        group = db.session.get(Group, value)
        if (
            user
            and group
            and user.username != get_jwt_identity()
            and value != Groups.admins.value
        ):
            user.groups.remove(group)
            db.session.commit()
            return {"message": "Removed"}, 200
        return {"message": "Denied"}, 403


bp.add_url_rule("/group/<value>/<int:user_id>", view_func=GroupView.as_view("group"))


class RoleView(MethodView):
    """
    Get a user's role based on the value and user ID.
    """

    decorators = [roles_required(Roles.admin.value), bp.doc(hide=True)]

    def get(self, value, user_id):
        user = db.session.get(User, user_id)
        if user and value not in user.roles:
            user.roles.append(Role.get_role(value))
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
            and user.username != get_jwt_identity()
            and value != Roles.admin.value
        ):
            user.roles.remove(role)
            db.session.commit()
            return {"message": "Removed"}, 200
        return {"message": "Denied"}, 403


bp.add_url_rule("/role/<value>/<int:user_id>", view_func=RoleView.as_view("role"))


class TableView(MethodView):
    decorators = [group_required(Groups.admins.value), bp.doc(hide=True)]

    def get(self, item, num):
        model = models_schemas[item][0]
        schema = models_schemas[item][1]

        query = select(model).order_by(model.id.desc())
        search_data = request.args.get("search")
        if search_data:
            query = query.filter_by(id=search_data)
        result = db.paginate(
            query,
            page=num,
            per_page=current_app.config["PAGINATION"],
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


bp.add_url_rule("/table/<item>/<int:num>", view_func=TableView.as_view("table"))
