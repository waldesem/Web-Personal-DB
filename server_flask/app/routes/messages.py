"""Route messages."""

from typing import ClassVar

from flask import Blueprint, Response, jsonify
from flask.views import MethodView
from sqlalchemy import select, text

from app.depends.depend import current_user, jwt_required
from app.model.tables import Messages, db_session

bp = Blueprint("messages", __name__)


class MessagesRoute(MethodView):
    """Message routes."""

    decorators: ClassVar = [jwt_required()]

    def get(self) -> Response:
        """Get messages."""
        messages = db_session.execute(
            select(Messages).filter(Messages.user_id == current_user.id).limit(12),
        ).scalars()
        return jsonify([row.to_dict() for row in messages]), 200

    def delete(self) -> Response:
        """Delete messages."""
        db_session.execute(
            text("DELETE FROM messages WHERE user_id = :user_id"),
            {"user_id": current_user.id},
        )
        db_session.commit()
        return "", 201


bp.add_url_rule("/messages", view_func=MessagesRoute.as_view("messages"))
