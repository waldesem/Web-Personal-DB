from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView

from . import bp
from config import Config
from ..tools.depends import jwt_required
from ..tools.queries import select_all, execute


class ConnnectView(MethodView):
    decorators = [jwt_required()]

    def get(self, page):
        """
        Retrieves a paginated list of Connect objects based on the specified group and item.
        """
        search_data = request.args.get("search", "")
        offset = (page - 1) * Config.PAGINATION
        limit = Config.PAGINATION + 1
        query = "SELECT * FROM connects"
        if search_data:
            query += " WHERE company LIKE '%{}%'".format(search_data)
        query += " ORDER BY id DESC LIMIT ? OFFSET ?"
        result = select_all(query, (limit, offset,))
        has_next = len(result) > Config.PAGINATION
        result = result[:Config.PAGINATION] if has_next else result
        names = select_all("SELECT DISTINCT name FROM connects ORDER BY name")
        companies = select_all(
            "SELECT DISTINCT company FROM connects ORDER BY company"
        )
        cities = select_all("SELECT DISTINCT city FROM connects ORDER BY city")
        return jsonify(
            {
                "contacts": result,
                "has_next": has_next,
                "has_prev": page > 1,
                "names": [n["name"] for n in names],
                "companies": [c["company"] for c in companies],
                "cities": [c["city"] for c in cities],
            }
        ), 200

    def post(self):
        """
        Create a new connection.
        """
        json_data = request.get_json()
        keys, args = zip(*json_data.items())
        query = "INSERT INTO connects ({}) VALUES ({})".format(
            ",".join(keys),
            ",".join("?" for _ in keys)
        )
        execute(query, args)
        return "", 201


    def patch(self, item_id):
        """
        Patch an item in the connects table.
        """
        json_data = request.get_json()
        json_data["updated"] = datetime.now()
        query_parts = ', '.join(key + '=?' for key in json_data.keys())
        args = tuple(json_data.values()) + (item_id,)
        query = f"UPDATE connects SET {query_parts} WHERE id = ?"
        execute(query, args)
        return "", 201

    def delete(self, item_id):
        """
        Deletes an item from the database.
        """
        execute("DELETE FROM connects WHERE id = ?", (item_id,))
        return "", 204


contacts_view = ConnnectView.as_view("connect")
bp.add_url_rule("/connect/<int:page>", view_func=contacts_view, methods=["GET"])
bp.add_url_rule("/connect", view_func=contacts_view, methods=["POST"])
bp.add_url_rule(
    "/connect/<int:item_id>",
    view_func=contacts_view,
    methods=["PATCH", "DELETE"],
)
