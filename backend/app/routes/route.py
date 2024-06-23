import json
import os
import re
import sqlite3
from datetime import datetime, timezone

from config import Config
from flask import abort, jsonify, request, send_file
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
from ..databases.database import execute, select
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
        views, companies, cities = [], [], []
        if result:
            views, companies, cities = [list(set(res)) for res in zip(*result)]
        return jsonify(
            {
                "view": views,
                "companies": companies,
                "cities": cities,
            }
        ), 200


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


@bp.get("/information")
@jwt_required()
def get_information():
    query_data = request.args
    result = select(
        """
        SELECT checks.conclusion, count(checks.id) FROM checks
            LEFT JOIN persons on checks.person_id = persons.id
            WHERE persons.region = ?
            AND checks.created BETWEEN ? AND ?
            GROUP BY conclusion
        """,
        many=True,
        args=(
            query_data["region"],
            query_data["start"],
            query_data["end"],
        ),
    )
    return jsonify(result), 200


@bp.post("/login/<action>")
def post_login(action):
    json_data = request.get_json()
    user = select(
        "SELECT * FROM users WHERE username = ?", args=(json_data.get("username"),)
    )
    if not user or user["blocked"] or user["deleted"]:
        return "", 204

    args = []
    stmt = "UPDATE users SET "
    if not check_password_hash(user["password"], json_data["password"]):
        if user["attempt"] < 5:
            stmt += "attempt = ? "
            args.append(user["attempt"] + 1)
        else:
            stmt += "blocked = 1 "
        args.append(user["id"])
        execute(stmt + "WHERE id = ?", tuple(args))
        return "", 204

    if action == "update":
        stmt += "password = ?, change_pswd = 0, attempt = 0 WHERE id = ?"
        args.extend([generate_password_hash(json_data["new_pswd"]), user["id"]])
        execute(stmt, tuple(args))
        return "", 201

    else:
        delta_change = datetime.now() - datetime.fromisoformat(user["pswd_create"])
        if not user["change_pswd"] and delta_change.days < 30:
            stmt += "last_login = ?, attempt = 0 WHERE id = ?"
            args.extend([datetime.now(timezone.utc), user["id"]])
            execute(stmt, tuple(args))
            return jsonify(
                {
                    "user_token": create_token(user),
                }
            ), 200
        return "", 205


@bp.get("/index/<int:page>")
@user_required()
def get_index(page):
    stmt = """
        SELECT persons.*, users.fullname AS username FROM persons 
        LEFT JOIN users ON persons.user_id = users.id 
        """
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

    result = select(stmt, many=True)
    has_next = len(result) > Config.PAGINATION
    result = result[: Config.PAGINATION] if has_next else result

    return jsonify([result, has_next, page > 1]), 200


@bp.get("/image/<int:item_id>")
def get_image(item_id):
    person_path = select("SELECT path FROM persons WHERE id = ?", args=(item_id,))
    if person_path.get("path"):
        file_path = os.path.join(person_path["path"], "image", "image.jpg")
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")


@bp.post("/file/<item>/<int:item_id>")
@jwt_required()
def post_file(item, item_id):
    file = request.files["file"]
    if not file.filename:
        return abort(400)

    if item == "persons":
        json_dict = json.load(file)
        person_id = update_person(json_dict)
        if person_id:
            return jsonify({"person_id": person_id}), 201
        return abort(400)

    person = select("SELECT * FROM persons WHERE id = ?", args=(item_id,))
    folders = Folders(
        person["region"],
        person["id"],
        person["surname"],
        person["firstname"],
        person.get("patronymic", ""),
    )

    if item == "image":
        folder = folders.create_parent_folder("image")
        endwith = file.filename.split(".")[-1]
        image_path = os.path.join(folder, "image." + endwith)

        if os.path.isfile(image_path):
            os.remove(image_path)
        file.save(image_path)
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
        user = select(
            "SELECT * FROM users WHERE username = ?", args=(json_dict.get("username"),)
        )
        if user and not json_dict["id"]:
            return "", 205

        if not json_dict["id"]:
            json_dict["password"] = generate_password_hash(Config.DEFAULT_PASSWORD)

        keys, args = zip(*json_dict.items())
        query = "INSERT OR REPLACE INTO users ({}) VALUES ({})".format(
            ",".join(keys), ",".join("?" for _ in keys)
        )
        print(query)
        execute(query, args)
        return "", 201

    except Exception as e:
        print(e)
        return "", 400


@bp.get("/users/<int:user_id>")
@jwt_required()
def get_user_id(user_id):
    if request.args.get("action") == "drop":
        execute(
            "UPDATE users SET password = ?, attempt = 0, blocked = 0, change_pswd = 1 WHERE id = ?",
            (
                generate_password_hash(Config.DEFAULT_PASSWORD),
                user_id,
            ),
        )
    stmt = "SELECT * FROM users WHERE id = ?"
    result = select(stmt, args=(user_id,))
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
    person = select(
        """SELECT persons.*, users.fullname AS username FROM persons
        LEFT JOIN users ON persons.user_id = users.id WHERE persons.id = ?""",
        args=(person_id,),
    )
    return jsonify(person), 200


@bp.get("/<item>")
@jwt_required()
def get_item(item):
    # Get users or contacts list with optional search query
    search_data = request.args.get("search")
    stmt = f"SELECT * FROM {item} "
    if search_data and len(search_data) > 2:
        if item == "users":
            stmt += "WHERE username LIKE '%{}%' ".format(search_data)
        else:
            stmt += "WHERE company LIKE '%{}%' ".format(search_data)
    result = select(stmt + "ORDER BY id DESC", many=True)
    return jsonify(result), 200


@bp.get("/<item>/<int:item_id>")
@jwt_required()
def get_item_id(item, item_id):
    if item in ["checks", "poligrafs", "inquiries", "investigations"]:
        stmt = f"SELECT *, users.fullname AS user FROM {item} LEFT JOIN users ON {item}.user_id = users.id "
    else:
        stmt = f"SELECT * FROM {item} "
    results = select(
        stmt + "WHERE person_id = ? ORDER BY id DESC", many=True, args=(item_id,)
    )
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
        execute(stmt, args)

        if item == "checks":
            args = []
            if not json_dict.get("conclusion"):
                args.extend([Statuses.saved.value, item_id])
            elif json_dict.get("pfo"):
                args.extend([Statuses.poligraf.value, item_id])
            else:
                args.extend([Statuses.finish.value, item_id])
            execute("UPDATE persons SET status = ? WHERE id = ?", tuple(args))

        if item == "poligrafs":
            stmt = "UPDATE persons SET status = CASE WHEN status = ? THEN ? ELSE status END WHERE id = ?"
            args = (
                Statuses.poligraf.value,
                Statuses.finish.value,
                item_id,
            )
            execute(stmt, args)

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
