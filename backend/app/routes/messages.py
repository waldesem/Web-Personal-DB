from flask import jsonify
from flask.views import MethodView

from . import bp
from ..utils.queries import select_all, execute
from ..utils.dependencies import Token, jwt_required


class MessageView(MethodView):
    decorators = [jwt_required()]

    def get(self):
        """
        Get the serialized representation of the messages.
        """
        return jsonify(select_all(
            "SELECT * FROM messages WHERE user_id = ? ORDER BY created DESC LIMIT 100"
        )), 200

    def delete(self, item_id):
        """
        Deletes the current instance of the resource from the database.
        """
        if not item_id:
            execute("DELETE FROM messages WHERE user_id = ?", (Token.current_user.id,))
        else:
            execute("DELETE FROM messages WHERE id = ?", (item_id,))
        return "", 204


message_view = MessageView.as_view("messages")
bp.add_url_rule("/messages", view_func=message_view, methods=["GET"])
bp.add_url_rule("/messages/<int:item_id>", view_func=message_view, methods=["DELETE"])
