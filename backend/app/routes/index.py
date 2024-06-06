import os

from flask import jsonify, request, send_file
from flask.views import MethodView

from . import bp
from config import Config
from ..tools.folders import Folders
from ..tools.depends import Token, jwt_required
from ..tools.queries import select_all, select_single
from ..tools.classes import Conclusions, Regions, Statuses


class IndexView(MethodView):
    @jwt_required()
    def get(self, flag, page):
        search_data = request.args.get("search")
        if flag == "search":
            if Token.current_user["region"] != Regions.main.name:
                result = select_all(
                    "SELECT * FROM person WHERE region = ? AND surname LIKE %{}% \
                        LEFT JOIN users on users.id = person.user_id \
                            ORDER BY {} {} OFFSET {} LIMIT {}".format(
                        request.args.get("sort"),
                        request.args.get("order"),
                        search_data,
                        page - 1,
                        Config.PAGINATION + 1,
                    ),
                    (Token.current_user["region"],),
                )
            else:
                result = select_all(
                    "SELECT * FROM person WHERE region = ? AND surname LIKE %{}% \
                        ORDER BY {} {} OFFSET {} LIMIT {}".format(
                        request.args.get("sort"),
                        request.args.get("order"),
                        search_data,
                        page - 1,
                        Config.PAGINATION + 1,
                    ),
                )

        elif flag == "officer":
            result = select_all(
                "SELECT * FROM person WHERE status NOT IN (?, ?) AND user_id = ? \
                    ORDER BY {} {} OFFSET {} LIMIT {}".format(
                    request.args.get("sort"),
                    request.args.get("order"),
                    page - 1,
                    Config.PAGINATION + 1,
                ),
                (Statuses.finish.name, Statuses.cancel.name, Token.current_user["id"]),
            )
        has_next = True if len(result) > Config.PAGINATION else False
        return jsonify(
            {
                "persons": result if not has_next else result[:-1],
                "has_next": has_next,
                "has_prev": True if page > 1 else False,
            }
        )


bp.add_url_rule("/index/<flag>/<int:page>", view_func=IndexView.as_view("index"))


class InformationView(MethodView):
    @jwt_required()
    def get(query_data):
        query_data = request.args
        result = select_all(
            "SELECT checks.conclusion, count(checks.id) FROM checks \
                LEFT JOIN person on checks.person_id = person.id \
                    WHERE person.region = ? \
                        AND checks.deadline BETWEEN ? AND ? \
                            GROUP BY conclusion",
            (
                query_data["region"],
                query_data["start"],
                query_data["end"],
            ),
        )
        return jsonify(result)


bp.add_url_rule("/information", view_func=InformationView.as_view("information"))


@jwt_required()
@bp.route("/image/<int:item_id>")
def get_image(item_id):
    """
    Retrieves a file from the server and sends it as a response.
    """
    person = select_single("SELECT * FROM person WHERE id = ?", (item_id,))
    folders = Folders(
        person["id"], person["surname"], person["firstname"], person["patronymic"]
    )
    file_path = os.path.join(folders.create_main_folder(), "image", "image.jpg")
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")


@bp.get("/classes")
def get_classes():
    results = [
        {item.name: item.value for item in items} 
        for items in [Regions, Statuses, Conclusions]
    ]
    return jsonify(results)
