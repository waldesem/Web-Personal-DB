from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView

from . import bp
from config import Config
from ..utils.dependencies import roles_required
from ..utils.queries import select_all, execute
from ..models.classes import Roles


class ConnnectView(MethodView):
    decorators = [roles_required(Roles.user.value)]

    def get(self, page):
        """
        Retrieves a paginated list of Connect objects based on the specified group and item.
        """
        search_data = request.args.get("search")
        result = select_all(
            "SELECT * FROM connects ORDER BY id DESC OFFSET ? LIMIT ?",
            (page - 1, Config.PAGINATION,),
        )
        if search_data:
            result = select_all(
                "SELECT * FROM connects WHERE company LIKE '%{}%' ORDER BY id DESC OFFSET ? LIMIT ?".format(
                    search_data
                ),
                (page - 1, Config.PAGINATION,),
            )
        has_next = True if len(result) > Config.PAGINATION else False
        names = select_all("SELECT DISTINCT name FROM connects ORDER BY name")
        companies = select_all(
            "SELECT DISTINCT company FROM connects ORDER BY company"
        )
        cities = select_all("SELECT DISTINCT city fROM connects ORDER BY city")
        return jsonify(
            {
                "contacts": result if not has_next else result[:-1],
                "has_next": has_next,
                "has_prev": True if page > 1 else False,
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
        execute(
            f"INSERT INTO connects ({','.join(json_data.keys())}, data) VALUES ({','.join(['?']*len(json_data))})",
            (",".join(json_data.values()), datetime.now()),
        )
        return jsonify({"message": "Created"}), 201

    def patch(self, item_id):
        """
        Patch an item in the connects table.
        """
        json_data = request.get_json()
        json_data["data"] = datetime.now()
        execute(
            f"UPDATE connects SET {','.join(key + '=?' for key in json_data.keys())} WHERE id = ?",
            tuple(json_data.values()) + (item_id,),
        )
        return jsonify({"message": "Updated"}), 201

    def delete(self, item_id):
        """
        Deletes an item from the database.
        """
        execute(f"DELETE FROM connects WHERE id = {item_id}")
        return jsonify({"message": "Deleted"}), 204


contacts_view = ConnnectView.as_view("connect")
bp.add_url_rule("/connect/<int:page>", view_func=contacts_view, methods=["GET"])
bp.add_url_rule("/connect", view_func=contacts_view, methods=["POST"])
bp.add_url_rule(
    "/connect/<int:item_id>",
    view_func=contacts_view,
    methods=["PATCH", "DELETE"],
)
