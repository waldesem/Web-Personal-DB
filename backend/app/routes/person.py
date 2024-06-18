from datetime import datetime

from flask import jsonify, request

from . import bp
from ..models.models import Prev, models_tables
from ..classes.classes import Statuses, Relations
from ..tools.depends import current_user, jwt_required, user_required
from ..tools.parsers import Resume
from ..tools.queries import execute, select_all, select_single


@bp.get("/resume/<int:person_id>")
@user_required()
def get_resume(person_id):
    if request.args.get("action") == "self":
        execute(
            "UPDATE persons SET status = ?, user_id = ? WHERE id = ?",
            (
                Statuses.manual.value,
                current_user["id"],
                person_id,
            ),
        )
    person = select_single(
        "SELECT * FROM persons WHERE id = ?",
        (person_id,),
    )
    if person["user_id"]:
        user_fullname = select_single(
            "SELECT fullname FROM users WHERE id = ?", (person["user_id"],)
        )
        person["username"] = user_fullname["fullname"]
    return jsonify(person), 200


@bp.post("/resume")
@user_required()
def post_resume():
    json_data = request.get_json()
    resume = Resume(json_data)
    person_id = resume.update_status()
    return jsonify({"person_id": person_id}), 201


@bp.delete("/resume/<int:person_id>")
@jwt_required()
def delete_resume(person_id):
    execute("DELETE FROM persons WHERE id = ?", (person_id,))
    return "", 204


@bp.post("/relations/<int:item_id>")
@jwt_required()
def post_relation(item_id):
    json_data = request.get_json()
    execute(
        "INSERT INTO relations (relation, relation_id) VALUES(?, ?, ?)",
        [
            (
                json_data["relation"],
                json_data["relation_id"],
                item_id,
            ),
            (
                json_data["relation"],
                item_id,
                json_data["relation_id"],
            ),
        ],
    )
    return "", 201


@bp.post("/previous/<int:item_id>")
@jwt_required()
def post_previous(item_id):
    json_data = request.get_json()
    try:
        json_dict = Prev(**json_data).dict() | {"person_id": item_id}
        person = select_single("SELECT * FROM persons WHERE id = ?", (item_id,))
        exist = Resume.get_person(
            json_dict["surname"],
            json_dict["firstname"],
            json_dict.get("patronymic", ""),
            datetime.strptime(person["birthday"], "%Y-%m-%d").date(),
        )
        if exist:
            execute(
                "INSERT INTO relations (relation, relation_id, person_id) VALUES (?, ?, ?)",
                [
                    (
                        Relations.similar.name,
                        exist["id"],
                        item_id,
                    ),
                    (
                        Relations.similar.name,
                        item_id,
                        exist["id"],
                    ),
                ],
            )
        keys, args = zip(*json_dict.items())
        stmt = "INSERT INTO previous ({}) VALUES ({})".format(
            ",".join(keys), ",".join(["?"] * len(keys))
        )
        execute(stmt, args)
        return "", 201
    except Exception as e:
        return str(e), 400


@bp.get("/<item>/<int:item_id>")
@jwt_required()
def get_items(item, item_id):
    results = select_all(
        f"SELECT * FROM {item} WHERE person_id = ? ORDER BY id ASC",
        (item_id,),
    )
    if item in ["checks", "poligrafs", "inquiries", "investigations"]:
        users = select_all("SELECT id, fullname FROM users")
        names = {user["id"]: user["fullname"] for user in users}
        for res in results:
            if "user_id" in res:
                res["user"] = names.get(res["user_id"])
    return jsonify(results)


@bp.post("/<item>/<int:item_id>")
@user_required()
def post_item(item, item_id):
    json_data = request.get_json()
    try:
        json_dict = models_tables[item](**json_data).dict()
        json_dict["person_id"] = item_id
        if item in ["checks", "poligrafs", "inquiries", "investigations"]:
            json_dict["user_id"] = current_user["id"]
        keys, args = zip(*json_dict.items())
        stmt = "INSERT OR REPLACE INTO {} ({}) VALUES ({})".format(
            item, ",".join(keys), ",".join(["?"] * len(keys))
        )
        execute(stmt, args)

        if item in ["checks", "poligrafs"] and not json_dict['id']:
            args = []
            if item == "checks":
                if json_dict.get("pfo"):
                    args.extend([Statuses.poligraf.value, item_id])
                else:
                    args.extend([Statuses.finish.value, item_id])
            if item == "poligrafs":
                person = select_single(
                    "SELECT status FROM persons WHERE id = ?", (item_id,)
                )
                if person["status"] == Statuses.poligraf.value:
                    args.extend([Statuses.finish.value, item_id])
            if args:
                execute("UPDATE persons SET status = ? WHERE id = ?", tuple(args))
        return "", 201
    except Exception as e:
        return str(e), 400


@bp.delete("/<item>/<int:item_id>")
@jwt_required()
def delete_item(item, item_id):
    execute(
        f"DELETE FROM {item} WHERE id = ?",
        (item_id,),
    )
    return "", 204
