import json
import os
import re
import sqlite3
from datetime import datetime, timezone

from config import Config
from flask import abort, jsonify, request, send_file
from PIL import Image
from werkzeug.security import check_password_hash, generate_password_hash

from ..classes.classes import (
    Addresses,
    Affiliates,
    Conclusions,
    Contacts,
    Documents,
    Educations,
    Poligrafs,
    Regions,
    Relations,
    Statuses,
)
from ..models.models import Connects, User, models_tables
from ..depends.depend import create_token, current_user, jwt_required, user_required
from ..tools.foldered import Folders
from ..tools.personed import update_resume, update_person
from ..databases.database import execute, select_all, select_single
from . import bp


@bp.get("/", defaults={"path": ""})
def main(path=""):
    return bp.send_static_file("index.html")


@bp.get("/<path:path>")
def static_file(path=""):
    return bp.send_static_file(path)


@bp.get("/classes")
def get_classes():
    results = [
        {item.name: item.value for item in items}
        for items in [
            Regions,
            Statuses,
            Conclusions,
            Relations,
            Affiliates,
            Educations,
            Addresses,
            Contacts,
            Documents,
            Poligrafs,
        ]
    ]
    return jsonify(results), 200


@bp.route("/connectors")
def get_connectors():
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        cur = conn.cursor()
        cur.execute("SELECT view, company, city FROM connects")
        result = cur.fetchall()
        view, company, city = [], [], []
        if result:
            views, companies, cities = [list(set(res)) for res in zip(*result)]
        return jsonify(
            {
                "view": views,
                "companies": companies,
                "cities": cities,
            }
        ), 200


@bp.get("/information")
@jwt_required()
def get_information():
    query_data = request.args
    result = select_all(
        """
        SELECT checks.conclusion, count(checks.id) FROM checks
            LEFT JOIN persons on checks.person_id = persons.id
            WHERE persons.region = ?
            AND checks.created BETWEEN ? AND ?
            GROUP BY conclusion
        """,
        (
            query_data["region"],
            query_data["start"],
            query_data["end"],
        ),
    )
    return jsonify(result), 200


@bp.post("/connects")
@jwt_required()
def post_connect():
    json_data = request.get_json()
    try:
        json_dict = Connects(**json_data).dict()
        keys, args = zip(*json_dict.items())
        query = "INSERT OR REPLACE INTO connects ({}) VALUES ({})".format(
            ",".join(keys), ",".join("?" for _ in keys)
        )
        execute(query, args)
        return "", 201

    except Exception as e:
        print(e)
        return "", 400


@bp.post("/login/<action>")
def post_login(action):
    json_data = request.get_json()
    user = select_single(
        "SELECT * FROM users WHERE username = ?", (json_data.get("username"),)
    )
    if not user or user["blocked"] or user["deleted"]:
        return "", 204

    if not check_password_hash(user["password"], json_data["password"]):
        if user["attempt"] < 5:
            execute(
                "UPDATE users SET attempt = ? WHERE id = ?",
                (
                    user["attempt"] + 1,
                    user["id"],
                ),
            )
        else:
            execute("UPDATE users SET blocked = 1 WHERE id = ?", (user["id"],))
        return "", 204

    if action == "update":
        execute(
            "UPDATE users SET password = ?, change_pswd = 0, attempt = 0 WHERE id = ?",
            (
                generate_password_hash(json_data["new_pswd"]),
                user["id"],
            ),
        )
        return "", 201

    else:
        delta_change = datetime.now(timezone.utc) - datetime.fromisoformat(
            user["pswd_create"]
        )
        if not user["change_pswd"] and delta_change.days < 30:
            execute(
                "UPDATE users SET last_login = ?, attempt = ? WHERE id = ?",
                (datetime.now(timezone.utc), 0, user["id"]),
            )
            return jsonify(
                {
                    "user_token": create_token(user),
                }
            ), 200
        return "", 205


@bp.get("/index/<int:page>")
@user_required()
def get_index(page):
    stmt = "SELECT * FROM persons "
    search_data = request.args.get("search")
    if search_data and len(search_data) > 2:

        if search_data.isdigit():
            stmt += "WHERE inn LIKE '%{}%' ".format(search_data)

        else:
            pattern = r"^\d{2}\.\d{2}\.\d{4}$"
            query = [
                search.strip().upper()
                for search in search_data.split(maxsplit=3)
                if search
            ]
            if len(query):
                stmt += "WHERE surname LIKE '%{}%' ".format(*query)
            if len(query) > 1 and not re.match(pattern, query[1]):
                stmt += "AND firstname LIKE '%{}%' ".format(query[1])
            if len(query) > 2 and not re.match(pattern, query[2]):
                stmt += "AND patronymic LIKE '%{}%' ".format(query)
            if len(query) > 1 and re.match(pattern, query[-1]):
                stmt += "AND birthday = '{}' ".format(
                    datetime.strptime(query[-1], "%d.%m.%Y").date()
                )

        if current_user["region"] != Regions.main.value:
            stmt += "AND region = {} ".format(current_user["region"])

    else:
        if current_user["region"] != Regions.main.value:
            stmt += "WHERE region = {} ".format(current_user["region"])

    stmt += "ORDER BY {} {} LIMIT {} OFFSET {}".format(
        request.args.get("sort"),
        request.args.get("order"),
        Config.PAGINATION + 1,
        (page - 1) * Config.PAGINATION,
    )

    result = select_all(stmt)
    has_next = len(result) > Config.PAGINATION
    if result:
        result = result[: Config.PAGINATION] if has_next else result
        users = select_all("SELECT id, fullname FROM users")
        names = {u["id"]: u["fullname"] for u in users}
        for i in result:
            if i["user_id"]:
                i["username"] = names[i["user_id"]]

    return jsonify([result, has_next, page > 1]), 200


@bp.get("/image/<int:item_id>")
def get_image(item_id):
    person_path = select_single("SELECT path FROM persons WHERE id = ?", (item_id,))
    if person_path.get("path"):
        file_path = os.path.join(person_path["path"], "image", "image.jpg")
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")


@bp.post("/file/<item>")
@bp.post("/file/<item>/<int:item_id>")
@user_required()
def post(item, item_id):
    file = request.files["file"]
    if not file.filename:
        return abort(400)

    if item == "anketa":
        json_dict = json.load(file)
        person_id = update_person(json_dict)
        if person_id:
            return "", 201
        return abort(400)

    person = select_single("SELECT * FROM persons WHERE id = ?", (item_id,))
    folders = Folders(
        current_user["region"],
        person["id"],
        person["surname"],
        person["firstname"],
        person.get("patronymic", ""),
    )

    if item == "image":
        folder = folders.create_parent_folder("image")
        im = Image.open(file)
        rgb_im = im.convert("RGB")
        image_path = os.path.join(folder, "image.jpg")

        if os.path.isfile(image_path):
            os.remove(image_path)
        rgb_im.save(image_path)
        return "", 201

    folder = folders.create_subfolder(item)
    files = request.files.getlist("file")
    for file in files:
        if file.filename:
            file_path = os.path.join(folder, file.filename)
            if not os.path.isfile(file_path):
                file.save(file_path)
    return "", 201


@bp.post("/users")
@jwt_required()
def post_user():
    json_data = request.get_json()
    try:
        json_dict = User(**json_data).dict()
        user = select_single(
            "SELECT * FROM users WHERE username = ?", (json_dict.get("username"),)
        )

        if user and not json_dict["id"]:
            return "", 205

        if not json_dict["id"]:
            json_dict["password"] = generate_password_hash(Config.DEFAULT_PASSWORD)

        keys, args = zip(*json_dict.items())
        query = "INSERT OR REPLACE INTO users ({}) VALUES ({})".format(
            ",".join(keys), ",".join("?" for _ in keys)
        )
        execute(query, args)
        return "", 201

    except Exception as e:
        print(e)
        return "", 400


@bp.get("/users/<int:user_id>")
@jwt_required()
def get_user_id(user_id):
    if request.args.get("action") == "drop":
        stmt = "UPDATE users SET password = ?, attempt = ?, blocked = ?, change_pswd = ? WHERE id = ? "
        values = (
            generate_password_hash(Config.DEFAULT_PASSWORD),
            0,
            False,
            True,
            user_id,
        )
        execute(stmt, values)

    stmt = "SELECT * FROM {item} WHERE id = ?"
    result = select_single(stmt, (user_id,))
    return jsonify(result), 200


@bp.post("/persons")
@user_required()
def post_resume():
    """
    Creates a new user, person or contact based on the provided JSON data.
    """
    json_data = request.get_json()
    person_id = update_resume(json_data)
    return jsonify({"person_id": person_id}), 201


@bp.get("/persons/<int:person_id>")
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


@bp.get("/<item>")
@jwt_required()
def get_item(item):
    search_data = request.args.get("search")
    stmt = f"SELECT * FROM {item} "

    if search_data and len(search_data) > 2:
        if item == "users":
            stmt += "WHERE username LIKE '%{}%' ".format(search_data)
        else:
            stmt += "WHERE company LIKE '%{}%' ".format(search_data)

    result = select_all(stmt + "ORDER BY id DESC")
    return jsonify(result), 200


@bp.get("/<item>/<int:item_id>")
@jwt_required()
def get_item_id(item, item_id):
    stmt = "SELECT * FROM {item} WHERE person_id = ? ORDER BY id DESC"
    results = select_all(stmt, (item_id,))

    if item in ["checks", "poligrafs", "inquiries", "investigations"]:
        users = select_all("SELECT id, fullname FROM users")
        names = {user["id"]: user["fullname"] for user in users}
        for res in results:
            if "user_id" in res:
                res["user"] = names.get(res["user_id"])
    return jsonify(results), 200


@bp.post("/<item>/<int:item_id>")
@user_required()
def post_item_id(item, item_id):
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

        if item == "relations":
            args = [
                args,
                (
                    json_data["relation"],
                    item_id,
                    json_data["relation_id"],
                ),
            ]
        execute(stmt, args)

        if item in ["checks", "poligrafs"] and not json_dict["id"]:
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
@user_required()
def delete_item(item, item_id):
    stmt = "DELETE FROM {} WHERE id = ?".format(item)
    if item == "users":
        stmt = "UPDATE users SET deleted = 1 WHERE id = ?"
    execute(stmt, (item_id,))
    return "", 204
