import sqlite3
from flask import jsonify
from flask.views import MethodView

from config import Config
from . import bp
from ..utils.dependencies import Token, jwt_required


class MessageView(MethodView):
    decorators = [jwt_required()]

    def get(self):
        """
        Get the serialized representation of the messages.
        """
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query = cursor.execute(
                "SELECT * FROM messages WHERE user_id = ? ORDER BY created DESC LIMIT 100"
            )
            col_names = [i[0] for i in query.description]
            return jsonify(zip(col_names, query.fetchall()))

    def delete(self, item_id):
        """
        Deletes the current instance of the resource from the database.
        """
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            if not item_id:
                cursor.execute("DELETE FROM messages WHERE user_id = ?", (Token.current_user.id,))
            else:
                cursor.execute("DELETE FROM messages WHERE id = ?", (item_id,))
            conn.commit()
            return "", 204


message_view = MessageView.as_view("messages")
bp.add_url_rule("/messages", view_func=message_view, methods=["GET"])
bp.add_url_rule("/messages/<int:item_id>", view_func=message_view, methods=["DELETE"])
