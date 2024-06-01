from flask import abort, jsonify, request
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from config import Config
from . import bp
from ..utils.dependencies import Token, roles_required, jwt_required
from ..models.classes import Roles
from ..models.model import engine, User, Role, Message


@roles_required(Roles.admin.value)
@bp.get("/users")
def get_users():
    """
    Endpoint to handle requests for getting users.
    """
    search_data = request.args.get("search")
    with Session(engine) as session:
        query = session.execute(
            select(User).filter_by(username=search_data).order_by(User.id.asc())
        ).all()
        return jsonify(q.__dict__ for q in query)


class UserView(MethodView):
    decorators = [roles_required(Roles.admin.value)]

    def get(self, user_id):
        """
        Retrieves a user based on the specified action and user ID.
        """
        action_data = request.args.get("action")
        with Session(engine) as session:
            if action_data != "view":
                user = session.get(User, user_id)
                match action_data:
                    case "block":
                        if user.username != Token.current_user.username:
                            user.blocked = not user.blocked
                    case "drop":
                        user.password = generate_password_hash(
                            Config.DEFAULT_PASSWORD, method="scrypt", salt_length=16
                        )
                        user.attempt = 0
                        user.pswd_change = None
                    case "region":
                        user.region_id = action_data
                    case _:
                        return abort, 404
                session.commit()
            user = session.get(User, user_id)
            return jsonify(user)

    def post(self):
        """
        Creates a new user based on the provided JSON data.
        """
        json_data = request.get_json()
        if not User.get_user(json_data.get("username")):
            with Session(engine) as session:
                session.add(
                    User(
                        fullname=json_data.get("fullname"),
                        username=json_data.get("username"),
                        email=json_data.get("email"),
                        password=generate_password_hash(
                            Config.DEFAULT_PASSWORD, method="scrypt", salt_length=16
                        ),
                    )
                )
                session.commit()
                return {"message": "Created"}, 201
        return {"message": "Denied"}, 403

    def patch(self, user_id, json_data):
        """
        Patch a user's information.
        """
        json_data = request.get_json()
        with Session(engine) as session:
            user = session.get(User, user_id)
            if user:
                for key, value in json_data.items():
                    setattr(user, key, value)
                session.commit()
                return {"message": "Changed"}, 201
        return {"message": "Denied"}, 403

    def delete(self, user_id):
        """
        Delete a user by their ID.
        """
        with Session(engine) as session:
            user = session.get(User, user_id)
            if user and user.username != Token.current_user.username:
                user.deleted = True
                session.commit()
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

    decorators = [roles_required(Roles.admin.value)]

    def get(self, value, user_id):
        with Session(engine) as session:
            user = session.get(User, user_id)
            role = session.get(Role, value)
            if user and role not in user.roles:
                user.roles.append(role)
                session.commit()
                return "", 201
        return "", 403

    def delete(self, value, user_id):
        """
        Deletes a role from a user.
        """
        with Session(engine) as session:
            user = session.get(User, user_id)
            role = session.get(Role, value)
            if (
                user
                and role
                and (
                    user.username != Token.current_user.username
                    or role.role != Roles.admin.value
                )
            ):
                user.roles.remove(role)
                session.commit()
                return "", 201
        return "", 403


bp.add_url_rule("/role/<value>/<int:user_id>", view_func=RoleView.as_view("role"))


class MessageView(MethodView):
    decorators = [jwt_required()]

    def get(self):
        """
        Get the serialized representation of the messages.
        """
        with Session(engine) as session:
            messages = session.execute(
                select(Message)
                .filter_by(user_id=Token.current_user.id)
                .order_by(Message.created.desc())
                .limit(100)
            ).all()
            return jsonify(
                message.__dict__.pop("_sa_instance_state", None) for message in messages
            )

    def delete(self, item_id):
        """
        Deletes the current instance of the resource from the database.
        """
        with Session(engine) as session:
            if not item_id:
                messages = (
                    session.execute(
                        select(Message).filter_by(user_id=Token.current_user.id)
                    )
                    .scalars()
                    .all()
                )
                if len(messages):
                    for message in messages:
                        session.delete(message)
            else:
                session.delete(session.get(Message, item_id))
            session.commit()
            return "", 204


message_view = MessageView.as_view("messages")
bp.add_url_rule("/messages", view_func=message_view, methods=["GET"])
bp.add_url_rule("/messages/<int:item_id>", view_func=message_view, methods=["DELETE"])
