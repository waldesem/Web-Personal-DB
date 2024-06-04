import os
import sqlite3

from flask import jsonify, request, send_file
from flask.views import MethodView

from . import bp
from config import Config
from ..utils.folders import Folders
from ..utils.dependencies import Token, roles_required
from ..utils.queries import select_from_table
from ..models.classes import Roles, Statuses


class IndexView(MethodView):
    @roles_required(Roles.user.value)
    def get(self, flag, page):
        search_data = request.args.get("search")
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            if flag == "search":
                if Token.current_user["region_id"] != 1:
                    query = cursor.execute(
                        f"SELECT * FROM person WHERE region_id = ? AND surname LIKE ? "
                        f"ORDER BY {request.args.get('sort')} {request.args.get('order')} "
                        f"OFFSET {page - 1} LIMIT {Config.PAGINATION + 1}",
                        (Token.current_user["region_id"], f"%{search_data}%"),
                    )
                else:
                    query = cursor.execute(
                        f"SELECT * FROM person WHERE surname LIKE ? "
                        f"ORDER BY {request.args.get('sort')} {request.args.get('order')} "
                        f"OFFSET {page - 1} LIMIT {Config.PAGINATION + 1}",
                        (f"%{search_data}%",),
                    )

            elif flag == "officer":
                query_finish = cursor.execute(
                    "SELECT id FROM statuses WHERE status = ?", (Statuses.finish.value,)
                )
                finish = query_finish.fetchone()[0]
                query_cancel = cursor.execute(
                    "SELECT id FROM statuses WHERE status = ?", (Statuses.cancel.value,)
                )
                cancel = query_cancel.fetchone()[0]
                query = cursor.execute(
                    "SELECT * FROM person WHERE status_id NOT IN (?, ?) AND user_id = ?",
                    (finish, cancel, Token.current_user["id"]),
                )

            col_names = [i[0] for i in query.description]
            result = [zip(col_names, q) for q in query.fetchall()]
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
        result = select_from_table(
            "fetchall",
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
        return jsonify(dict(map(lambda x: (x[1], x[0]), result)))


bp.add_url_rule("/information", view_func=InformationView.as_view("information"))


@roles_required(Roles.user.value)
@bp.route("/image/<int:item_id>")
def get_image(item_id):
    """
    Retrieves a file from the server and sends it as a response.
    """
    person = select_from_table(
        "fetchone", "SELECT * FROM person WHERE id = ?", (item_id,)
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
    result = []
    for table, item in tables_items.items():
        query = select_from_table("fetchall", f"SELECT id, {item} FROM {table}")
        result.append({q["id"]: q[item] for q in query})
    return jsonify(result)
