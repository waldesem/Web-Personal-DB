import json
import os
import re
from datetime import datetime

from flask import Blueprint, abort, current_app, jsonify, request, send_file
from sqlalchemy import desc, func, select
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
)
from ..depends.depend import (
    create_token,
    current_user,
    get_current_user,
    jwt_required,
    user_required,
)
from ..handles.handlers import (
    handle_get_item,
    handle_post_resume,
    handle_update_person,
)
from ..model.models import User, models_tables
from ..model.tables import Checks, Persons, Users, db_session, tables_models

bp = Blueprint("route", __name__)


@bp.get("/classes")
@jwt_required()
def get_classes():
    results = [
        {item.name: item.value for item in items}
        for items in [
            Regions,
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


@bp.get("/auth")
@user_required()
def get_auth():
    return jsonify(current_user.to_dict()), 200


@bp.get("/information")
@user_required()
def get_information():
    """
    Retrieves information based on the provided query parameters.

    Returns:
        A JSON response containing the count of checks for each conclusion within the specified date range and region.
        The JSON response has the following structure:
        The HTTP status code is 200 if the information is successfully retrieved.

    Raises:
        None

    This function requires the user to be authenticated.

    Parameters:
        None

    Query Parameters:
        start (str): The start date of the date range in the format "YYYY-MM-DD".
        end (str): The end date of the date range in the format "YYYY-MM-DD".
        region (str): The region to filter the checks by.

    """
    data = request.args
    result = db_session.execute(
        select(Checks.conclusion, func.count(Checks.id))
        .join(Persons, Checks.person_id == Persons.id)
        .filter(
            Checks.created.between(data["start"], data["end"]),
            Persons.region == data.get("region")
            if data.get("region")
            else current_user.region,
        )
        .group_by(Checks.conclusion)
    ).all()
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
    user = db_session.execute(
        select(Users).where(Users.username == json_data.get("username"))
    ).scalar_one_or_none()
    if not user or user.blocked or user.deleted:
        return abort(400)

    if not check_password_hash(user.passhash, json_data["password"]):
        if user.attempt < 5:
            user.attempt += 1
        else:
            user.blocked = True
        db_session.commit()
        return abort(400)

    if action == "update":
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$"
        if re.match(pattern, json_data["new_pswd"]):
            user.passhash = generate_password_hash(json_data["new_pswd"])
            user.change_pswd = False
            user.attempt = 0
            db_session.commit()
            return "", 201
        return "", 205

    delta_change = datetime.now() - user.pswd_create
    if not user.change_pswd and delta_change.days < 365:
        if user.attempt > 0:
            user.attempt = 0
            db_session.commit()
        return jsonify(
            {
                "user_token": create_token(user),
            }
        ), 200
    return "", 205


@bp.get("/users")
@user_required(admin=True)
def get_users():
    """
    Retrieves a list of users from the database based on the provided search criteria.

    Parameters:
        item (str): The table name from which to retrieve the users.

    Returns:
        tuple: A tuple containing the JSON-encoded list of users and the HTTP status code.
    """
    search_data = request.args.get("search")
    stmt = select(Users)
    if search_data and len(search_data) > 2:
        if re.match(r"^[a-zA-z]+", search_data):
            stmt = stmt.filter(Users.username.like("%" + search_data + "%"))
        else:
            stmt = stmt.filter(Users.fullname.like("%" + search_data + "%"))
    users = db_session.execute(stmt.order_by(desc(Users.id))).scalars()
    result = [user.to_dict() for user in users]
    return jsonify(result), 200


@bp.post("/users")
@user_required(admin=True)
def post_user():
    """
    Handles the POST request to create a user in the database.

    This function is a route handler for the '/users' endpoint with the HTTP method POST.
    It requires a valid token for authentication.

    Parameters:
        None

    Returns:
        - If the user already exists returns an empty response with status code 205.
        - Else generates a hashed password using the default password.
        Returns an empty response with status code 201.
        - If an exception occurs during the execution of the function,
        returns an empty response with status code 400.
    """
    json_data = request.get_json()
    try:
        json_dict = User(**json_data).dict()
        user = db_session.execute(
            select(Users).filter(Users.username == json_dict.get("username"))
        ).all()
        if user:
            return "", 205

        json_dict["passhash"] = generate_password_hash(
            current_app.config["DEFAULT_PASSWORD"]
        )
        db_session.add(Users(**json_dict))
        db_session.commit()
        return "", 201

    except Exception as e:
        print(e)
        return "", 400


@bp.get("/users/<int:user_id>")
@user_required(admin=True)
def get_user_actions(user_id):
    if current_user.id == user_id:
        return "", 205  # forbidden
    """
    Change a user's information in the database based on their user ID.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        The HTTP status code is 201.
    """
    user = db_session.get(Users, user_id)
    if request.args.get("action") == "drop":
        user.passhash = generate_password_hash(current_app.config["DEFAULT_PASSWORD"])
        user.attempt = 0
        user.blocked = False
        user.change_pswd = True
    elif request.args.get("action") == "admin":
        user.has_admin = not user.has_admin
    elif request.args.get("action") == "delete":
        user.deleted = not user.deleted
        get_current_user.cache_clear()
    db_session.commit()
    return "", 201


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
    cur_user = current_user
    pagination = 14
    search_data = request.args.get("search")
    stmt = select(Persons, Users.fullname)
    if search_data and len(search_data) > 2:
        if search_data.isdigit():
            stmt.filter(Persons.inn.ilike("%" + search_data + "%"))
        else:
            pattern = r"^\d{2}\.\d{2}\.\d{4}$"
            query = list(map(str.upper, search_data.split()))
            if len(query):
                stmt = stmt.filter(Persons.surname.ilike("%" + query[0] + "%"))
            if len(query) > 1 and not re.match(pattern, query[-1]):
                stmt = stmt.filter(Persons.firstname.ilike("%" + query[1] + "%"))
            if len(query) > 2 and not re.match(pattern, query[-1]):
                stmt = stmt.filter(Persons.patronymic.ilike("%" + query[2] + "%"))
            if len(query) > 1 and re.match(pattern, query[-1]):
                stmt = stmt.filter(
                    Persons.birthday == datetime.strptime(query[-1], "%d.%m.%Y").date()
                )
        if cur_user.region != Regions.main.value:
            stmt = stmt.filter(Persons.region == cur_user.region)
    else:
        if cur_user.region != Regions.main.value:
            stmt = stmt.filter(Persons.region == cur_user.region)
    query = db_session.execute(
        stmt.filter(Persons.user_id == Users.id)
        .order_by(desc(Persons.id))
        .limit(pagination + 1)
        .offset((page - 1) * pagination)
    ).all()
    result = [row[0].to_dict() | {"username": row[1]} for row in query]
    has_next = len(result) > pagination
    result = result[:pagination] if has_next else result
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
    person_path = db_session.execute(
        select(Persons.destination).where(Persons.id == item_id)
    ).scalar_one_or_none()
    if person_path:
        file_path = os.path.join(person_path, "image", "image.jpg")
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")


@bp.post("/file/<item>/<int:item_id>")
@user_required()
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

    person_dir = db_session.scalars(
        select(Persons.destination).filter(Persons.id == item_id)
    ).first()
    if not person_dir:
        return abort(400)
    try:
        if not os.path.isdir(person_dir):
            os.mkdir(person_dir)

        item_dir = os.path.join(person_dir, item)
        if not os.path.isdir(item_dir):
            os.mkdir(item_dir)

        if item == "image":
            endwith = file.filename.split(".")[-1]
            image_file = os.path.join(item_dir, "image." + endwith)
            if os.path.isfile(image_file):
                os.remove(image_file)
            file.save(image_file)
            return "", 201

        date_subfolder = os.path.join(
            item_dir,
            datetime.now().strftime("%Y-%m-%d"),
        )
        if not os.path.isdir(date_subfolder):
            os.mkdir(date_subfolder)

        files = request.files.getlist("file")
        for file in files:
            if file.filename:
                file_path = os.path.join(date_subfolder, file.filename)
                if not os.path.isfile(file_path):
                    file.save(file_path)
        return "", 201
    except OSError as e:
        print(e)
        return abort(400)


@bp.get("/profile/<int:person_id>")
@user_required()
def get_profile(person_id):
    """
    Retrieves all information related to a person in one request.

    Parameters:
        person_id (int): The ID of the person for whom to retrieve all information.

    Returns:
        List[Dict[str, Any]]:
        A list of dictionaries representing the person's
        information and an HTTP status code of 200.
    """
    result = [handle_get_item(item, person_id) for item in tables_models.keys()]
    return jsonify(result), 200


@bp.post("/resume")
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
    if item == "persons" and request.args.get("action") == "self":
        person = db_session.get(Persons, item_id)
        person.standing = not person.standing
        person.user_id = current_user.id
        db_session.commit()
    results = handle_get_item(item, item_id)
    return jsonify(results), 200


@bp.post("/<item>/<int:item_id>")
@user_required()
def post_item_id(item, item_id):
    """
    Inserts or replaces a record in the specified table with the given item ID.

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
    json_dict = models_tables[item](**json_data).dict()
    if item != "persons":
        json_dict["person_id"] = item_id
    json_dict["user_id"] = current_user.id
    db_session.merge(tables_models[item](**json_dict))
    db_session.commit()
    return "", 201


@bp.delete("/<item>/<int:item_id>")
@jwt_required()
def delete_item(item, item_id):
    """
    Deletes an item from the database based on the provided item name and item ID.

    Parameters:
        item (str): The name of the table to delete the item from.
        item_id (int): The ID of the item to delete.

    Returns:
        Tuple[str, int]: A tuple containing an empty string and an HTTP status
        code of 204 if the operation is successful or an HTTP status
        code of 400.
    """
    item = db_session.get(tables_models[item], item_id)
    if not item:
        return abort(400)
    db_session.delete(item)
    db_session.commit()
    return "", 204
