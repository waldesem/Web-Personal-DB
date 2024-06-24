import json
import os
import re
from datetime import datetime

from flask import abort, Blueprint, jsonify, request, send_file
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
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
from ..databases.database import execute, select
from ..depends.depend import create_token, current_user, jwt_required, user_required
from ..handles.handlers import (
    handle_get_item,
    handle_get_person,
    handle_post_resume,
    handle_update_person,
)
from ..models.models import User, models_tables
from ..tools.tool import Folders


bp = Blueprint("route", __name__)


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


@bp.get("/information")
@jwt_required()
def get_information():
    query_data = request.args
    result = select(
        """
        SELECT checks.conclusion, count(checks.id) as count FROM checks
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
    """
    A function that handles the login process.

    Parameters:
        action (str): The action to be performed during the login process.

    Returns:
        The function returns a tuple containing an empty string and a status code.
        The status code is either 204, 201, or 205, depending on the outcome of the login process.

    Raises:
        None
    """
    json_data = request.get_json()
    user = select(
        """
        SELECT id, username, password, blocked, deleted, attempt, pswd_create, change_pswd, has_admin
        FROM users WHERE username = ?
        """,
        args=(json_data.get("username"),),
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
            args.extend([datetime.now(), user["id"]])
            execute(stmt, tuple(args))
            return jsonify(
                {
                    "user_token": create_token(user),
                }
            ), 200
        return "", 205


@bp.get("/users")
@jwt_required()
def get_users():
    """
    Retrieves a list of users from the database based on the provided search criteria.

    Parameters:
        item (str): The table name from which to retrieve the users.

    Returns:
        tuple: A tuple containing the JSON-encoded list of users and the HTTP status code.
    """
    search_data = request.args.get("search")
    stmt = "SELECT id, fullname, username, blocked, deleted, pswd_create, last_login, region FROM users "
    if search_data and len(search_data) > 2:
        stmt += "WHERE username LIKE '%{}%' ".format(search_data)
    result = select(stmt + "ORDER BY id DESC", many=True)
    return jsonify(result), 200


@bp.post("/users")
@jwt_required()
def post_user():
    """
    Handles the POST request to create or update a user in the database.

    This function is a route handler for the '/users' endpoint with the HTTP method POST.
    It requires a valid JWT token for authentication.

    Parameters:
        None

    Returns:
        - If the user already exists and the request does not include an 'id' field, returns an empty response with status code 205.
        - If the request does not include an 'id' field, generates a hashed password using the default password from the Config module and inserts the user into the 'users' table.
        Returns an empty response with status code 201.
        - If an exception occurs during the execution of the function, prints the exception and returns an empty response with status code 400.
    """
    json_data = request.get_json()
    try:
        json_dict = User(**json_data).dict()
        user = select(
            "SELECT id FROM users WHERE username = ?", args=(json_dict.get("username"),)
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
    """
    Retrieves a user's information from the database based on their user ID.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        tuple: A tuple containing the user's information and the HTTP status code.
            The user's information is returned as a JSON object.
            The HTTP status code is 200 if the user is found, otherwise it is 404.
    """
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


@bp.get("/index/<int:page>")
@user_required()
def get_index(page):
    """
    Retrieves a paginated list of persons from the database based on the search
    query and the user's region.

    Parameters:
        page (int): The page number of the results.

    Returns:
        tuple: A tuple containing the list of persons, a boolean indicating if
        there are more results, and a boolean indicating if the page is greater
        than 1.

    Raises:
        None
    """
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

    stmt += "ORDER BY id LIMIT {} OFFSET {}".format(
        Config.PAGINATION + 1,
        (page - 1) * Config.PAGINATION,
    )

    result = select(stmt, many=True)
    has_next = len(result) > Config.PAGINATION
    result = result[: Config.PAGINATION] if has_next else result

    return jsonify([result, has_next, page > 1]), 200


@bp.get("/image/<int:item_id>")
def get_image(item_id):
    """
    Retrieves an image file associated with a person's ID.

    Args:
        item_id (int): The ID of the person.

    Returns:
        Response: A Flask Response object containing the image file.

    Raises:
        None.
    """
    person_path = select("SELECT path FROM persons WHERE id = ?", args=(item_id,))
    if person_path.get("path"):
        file_path = os.path.join(person_path["path"], "image", "image.jpg")
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")


@bp.post("/file/<item>/<int:item_id>")
@jwt_required()
def post_file(item, item_id):
    """
    Retrieves an image file associated with a person's ID.

    Args:
        item_id (int): The ID of the person.

    Returns:
        Response: A Flask Response object containing the image file.

    Raises:
        None.
    """
    file = request.files["file"]
    if not file.filename:
        return abort(400)

    if item == "persons":
        json_dict = json.load(file)
        person_id = handle_update_person(json_dict)
        if person_id:
            return jsonify({"person_id": person_id}), 201
        return abort(400)

    person = select(
        "SELECT id, region, surname, firstname, patronymic FROM persons WHERE id = ?",
        args=(item_id,),
    )
    folders = Folders(
        person.get("region"),
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


@bp.get("/allinone/<int:person_id>")
@user_required()
def get_all_in_one(person_id):
    """
    Retrieves all information related to a person in one request.

    This function takes a person_id as a parameter and retrieves all information
    related to that person, including their resume and other items.

    Parameters:
        person_id (int): The ID of the person for whom to retrieve all information.

    Returns:
        Tuple[List[Dict[str, Any]], int]:
        A tuple containing a list of dictionaries representing the person's i
        nformation and an HTTP status code of 200.
    """
    response = [handle_get_person(person_id)]
    for item in models_tables.keys():
        response.append(handle_get_item(item, person_id))
    return jsonify(response), 200


@bp.post("/persons")
@user_required()
def post_resume():
    """
    Creates a new user, person or contact based on the provided JSON data.

    Parameters:
        None

    Returns:
        A JSON response containing the person ID and an HTTP status code of 201.
        The person ID is the ID of the newly created user, person, or contact.
    """

    json_data = request.get_json()
    person_id = handle_post_resume(json_data)
    return jsonify({"person_id": person_id}), 201


@bp.get("/persons/<int:person_id>")
@user_required()
def get_resume(person_id):
    """
    Retrieves the resume of a person with the given person_id.

    If the query parameter "action" is set to "self", the function updates
    the status and user_id of the person with the given person_id in the database.

    Parameters:
        person_id (int): The ID of the person whose resume is to be retrieved.

    Returns:
        Tuple[Response, int]: A tuple containing the JSON response containing
        the person's resume and an HTTP status code of 200.
    """
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


@bp.get("/<item>/<int:item_id>")
@jwt_required()
def get_item_id(item, item_id):
    """
    Retrieves an item from the database based on the provided item name and item ID.

    Parameters:
        item (str): The name of the table to retrieve the item from.
        item_id (int): The ID of the item to retrieve.

    Returns:
        Tuple[Response, int]: A tuple containing the JSON response containing
        the retrieved item(s) and an HTTP status code of 200.
    """
    results = handle_get_item(item, item_id)
    return jsonify(results), 200


@bp.post("/<item>/<int:item_id>")
@user_required()
def post_item_id(item, item_id):
    """
    Inserts or replaces a record in the specified table with the given item ID.
    If the item is one of 'checks', 'poligrafs', 'inquiries', or 'investigations', 
    the 'user_id' field is set to the current user's ID.

    Parameters:
        item (str): The name of the table to insert or replace the record in.
        item_id (int): The ID of the record to insert or replace.

    Returns:
        Tuple[str, int]: A tuple containing an empty string and an HTTP status
        code of 201 if the operation is successful,
        otherwise a string containing the exception message and an HTTP status
        code of 400.
    """
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
    """
    Deletes an item from the database based on the provided item name and item ID.

    Parameters:
        item (str): The name of the table to delete the item from.
        item_id (int): The ID of the item to delete.

    Returns:
        Tuple[str, int]: A tuple containing an empty string and an HTTP status
        code of 204 if the operation is successful.
    """
    stmt = "DELETE FROM {} WHERE id = ?".format(item)
    if item == "users":
        stmt = "UPDATE users SET deleted = 1 WHERE id = ?"
    execute(stmt, (item_id,))
    return "", 204
