import os

from flask import jsonify, request, send_file

from . import bp
from config import Config
from ..tools.folders import Folders
from ..tools.depends import current_user, jwt_required, user_required
from ..tools.queries import select_all, select_single
from ..tools.classes import Conclusions, Regions, Statuses, Relations


@user_required()
@bp.route("/index/<flag>/<int:page>")
def get_index(flag, page):
    search_data = request.args.get("search", "")
    offset = (page - 1) * Config.PAGINATION
    limit = Config.PAGINATION + 1
    query = "SELECT * FROM persons "
    args = []
    if flag == "search":
        if search_data:
            query += "WHERE surname LIKE upper('%{}%') ".format(search_data.upper())
            if current_user["region"] != Regions.main.name:
                query += " AND region = ? "
                args.append(current_user["region"]) 
        else:
            if current_user["region"] != Regions.main.name:
                query += " WHERE region = ? "
                args.append(current_user["region"]) 
    if flag == "officer":
        query += "WHERE status = ? AND user_id = ? "
        args.extend([Statuses.manual.name, current_user["id"]])
    query += " ORDER BY {} {} LIMIT {} OFFSET {} ".format(
        request.args.get("sort"), request.args.get("order"), limit, offset
    )
    result = select_all(query, tuple(args) if args else (""))
    has_next = len(result) > Config.PAGINATION if result else False
    result = result[:Config.PAGINATION] if has_next else result
    users = select_all("SELECT id, fullname FROM users")
    names = {u["id"]: u["fullname"] for u in users}
    for i in result:
        if i["user_id"]:
            i["username"] = names[i["user_id"]]
    return jsonify(
        {
            "persons": result,
            "has_next": has_next,
            "has_prev": page > 1,
        }
    ), 200


@jwt_required()
@bp.route("/information")
def get_information(query_data):
    query_data = request.args
    result = select_all(
        "SELECT checks.conclusion, count(checks.id) FROM checks \
            LEFT JOIN persons on checks.person_id = persons.id \
                WHERE persons.region = ? \
                    AND checks.created BETWEEN ? AND ? \
                        GROUP BY conclusion",
        (
            query_data["region"],
            query_data["start"],
            query_data["end"],
        ),
    )
    return jsonify(result), 200


@jwt_required()
@bp.route("/image/<int:item_id>")
def get_image(item_id):
    """
    Retrieves a file from the server and sends it as a response.
    """
    person = select_single("SELECT * FROM persons WHERE id = ?", (item_id,))
    folders = Folders(
        person["id"], person["surname"], person["firstname"], person.get("patronymic", "")
    )
    file_path = os.path.join(folders.create_main_folder(), "image", "image.jpg")
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")


@bp.get("/classes")
def get_classes():
    results = [
        {item.name: item.value for item in items} 
        for items in [Regions, Statuses, Conclusions, Relations]
    ]
    return jsonify(results), 200
