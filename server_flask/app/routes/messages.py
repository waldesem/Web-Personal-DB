"""Route messages."""

from typing import ClassVar

from flask import Blueprint, Response, jsonify
from flask.views import MethodView
from sqlalchemy import desc, select

from app.depends.depend import current_user, jwt_required
from app.model.tables import Messages, db_session

bp = Blueprint("messages", __name__)


class MessagesRoute(MethodView):
    """Message routes."""

    decorators: ClassVar = [jwt_required]

    messages = db_session.execute(
        select(Messages).filter_by(user_id=current_user.id)
        .order_by(desc(Messages.id)),
    ).scalars()

    @jwt_required
    def get(self) -> Response:
        """Get messages."""
        return jsonify([row.to_dict() for row in self.messages]), 200

    @jwt_required
    def delete(self) -> Response:
        """Delete messages."""
        for row in self.messages:
            db_session.delete(row)
        return jsonify({"message": "Success"}), 201


bp.add_url_rule("/messages", view_func=MessagesRoute.as_view("messages"))
