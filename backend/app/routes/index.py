import os

from flask import jsonify, request, send_file
from flask.views import MethodView

from . import bp
from config import Config
from ..utils.folders import Folders
from ..utils.dependencies import Token, roles_required
from ..utils.queries import select_all, select_single
from ..models.classes import Roles, Statuses


class IndexView(MethodView):
    @roles_required(Roles.user.value)
    def get(self, flag, page):
        search_data = request.args.get("search")
        if flag == "search":
            if Token.current_user["region_id"] != 1:
                result = select_all(
                    f"SELECT * FROM person WHERE region_id = ? AND surname LIKE ? "
                    f"ORDER BY {request.args.get('sort')} {request.args.get('order')} "
                    f"OFFSET {page - 1} LIMIT {Config.PAGINATION + 1}",
                    (Token.current_user["region_id"], f"%{search_data}%"),
                )
            else:
                result = select_all(
                    f"SELECT * FROM person WHERE surname LIKE ? "
                    f"ORDER BY {request.args.get('sort')} {request.args.get('order')} "
                    f"OFFSET {page - 1} LIMIT {Config.PAGINATION + 1}",
                    (f"%{search_data}%",),
                )

        elif flag == "officer":
            finish = select_single(
                "SELECT id FROM statuses WHERE status = ?", (Statuses.finish.value,)
            )
            cancel = select_single(
                "SELECT id FROM statuses WHERE status = ?", (Statuses.cancel.value,)
            )
            result = select_all(
                "SELECT * FROM person WHERE status_id NOT IN (?, ?) AND user_id = ?",
                (finish['id'], cancel['id'], Token.current_user["id"]),
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
    @roles_required(Roles.user.value)
    def get(query_data):
        query_data = request.args
        result = select_all(
            "SELECT checks.conclusion_id, count(checks.id) FROM checks \
                LEFT JOIN person on checks.person_id = person.id \
                    WHERE person.region_id = ? \
                        AND checks.deadline BETWEEN ? AND ? \
                            GROUP BY conclusion_id",
            (
                query_data["region_id"],
                query_data["start"],
                query_data["end"],
            ),
        )
        return jsonify(result)


bp.add_url_rule("/information", view_func=InformationView.as_view("information"))


@roles_required(Roles.user.value)
@bp.route("/image/<int:item_id>")
def get_image(item_id):
    """
    Retrieves a file from the server and sends it as a response.
    """
    person = select_single("SELECT * FROM person WHERE id = ?", (item_id,)
    )
    folders = Folders(
        person["id"], person["surname"], person["firstname"], person["patronymic"]
    )
    file_path = os.path.join(folders.create_main_folder(), "image", "image.jpg")
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")


@bp.get("/classes")
def get_classes():
    tables_items = {
        "users": "fullname",
        "conclusions": "conclusion",
        "statuses": "status",
        "regions": "region",
    }
    results = []
    for table, item in tables_items.items():
        query = select_all(f"SELECT id, {item} FROM {table}")
        results.append({q["id"]: q[item] for q in query})
    return jsonify(results)
