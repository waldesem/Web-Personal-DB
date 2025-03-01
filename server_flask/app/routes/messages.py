"""Route messages."""

from typing import ClassVar

from flask import Blueprint, Response, jsonify
from flask.views import MethodView
from sqlalchemy import desc, select, text

from app.depends.depend import current_user, jwt_required
from app.model.tables import Messages, db_session

bp = Blueprint("messages", __name__)


class MessagesRoute(MethodView):
    """Message routes."""

    decorators: ClassVar = [jwt_required]

    @jwt_required
    def get(self) -> Response:
        """Get messages."""
        messages = db_session.execute(
            select(Messages)
            .filter_by(user_id=current_user.id)
            .order_by(desc(Messages.id))
            .limit(10),
        ).scalars()
        return jsonify([row.to_dict() for row in messages]), 200

    @jwt_required
    def delete(self) -> Response:
        """Delete messages."""
        db_session.execute(
            text("DELETE FROM messages WHERE user_id = :user_id"),
            {"user_id": current_user.id},
        )
        return "", 201


bp.add_url_rule("/messages", view_func=MessagesRoute.as_view("messages"))
