from datetime import datetime
import json
import os
import re
import shutil
import subprocess

from flask import Blueprint, abort, current_app, jsonify, request, send_file
from sqlalchemy import desc, func, select
from werkzeug.security import check_password_hash, generate_password_hash

from ..depends.depend import (
    create_token,
    current_user,
    get_current_user,
    jwt_required,
    roles_required,
)
from ..model.classes import Regions, Roles
from ..model.models import Person, User
from ..model.tables import Checks, Persons, Users, db_session, tables_models
from ..handlers.handler import (
    handle_image,
    handle_json_to_dict,
    handle_get_item,
    handle_post_item,
    handle_post_resume,
    make_destination,
)

bp = Blueprint("route", __name__, url_prefix="/api")


@bp.post("/login/<action>")
def post_login(action):
    """
    A function that handles the login process.

    Parameters:
        action (str): The action to be performed during the login process.

    Returns:
        The function returns a tuple containing an empty string and a status code.
        The status code is either 204, or 205, depending on the outcome of the login process.

    Raises:
        None
    """
    json_data = request.get_json()
    user = db_session.execute(
        select(Users).where(Users.username == json_data.get("username"))
    ).scalar_one_or_none()
    if not user or user.blocked or user.deleted:
        return {"message": "Invalid"}

    if not check_password_hash(user.passhash, json_data["password"]):
        if user.attempt < 5:
            user.attempt += 1
        else:
            user.blocked = True
        db_session.commit()
        return {"message": "Invalid"}

    if action == "update":
        user.passhash = generate_password_hash(json_data["new_pswd"])
        user.change_pswd = False
        user.attempt = 0
        db_session.commit()
        return {"message": "Updated"}

    delta_change = datetime.now() - user.pswd_create
    if not user.change_pswd and delta_change.days < 365:
        if user.attempt > 0:
            user.attempt = 0
            db_session.commit()
        return jsonify(
            {
                "message": "Success",
                "user_token": create_token(User(**user.to_dict()).dict()),
            }
        )
    return {"message": "Denied"}


@bp.get("/logout")
@jwt_required()
def get_logout():
    """
    A function that handles the logout process.

    Parameters:
        None

    Returns:
        The function returns a tuple containing an empty string and a status code.
        The status code is either 204, or 205, depending on the outcome of the logout process.

    Raises:
        None
    """
    get_current_user.cache_clear()
    return {"message": "Success"}


@bp.get("/users")
@roles_required(Roles.admin.value)
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
        if re.match(r"^[a-zA-z_]+", search_data):
            stmt = stmt.filter(Users.username.like("%" + search_data + "%"))
        else:
            stmt = stmt.filter(Users.fullname.like("%" + search_data + "%"))
    users = db_session.execute(stmt.order_by(desc(Users.id))).scalars()
    return jsonify([user.to_dict() for user in users]), 200


@bp.post("/users")
@roles_required(Roles.admin.value)
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
        if not user:
            json_dict["role"] = Roles.guest.value
            json_dict["region"] = Regions.main.value
            json_dict["passhash"] = generate_password_hash(
                current_app.config["DEFAULT_PASSWORD"]
            )
            db_session.add(Users(**json_dict))
            db_session.commit()
            return "", 201
        return abort(400)
    except Exception as e:
        print(e)
        return abort(400)


@bp.get("/users/<int:user_id>")
@roles_required(Roles.admin.value)
def get_user_actions(user_id):
    if current_user.get("id") == user_id:
        return abort(400)
    """
    Change a user's information in the database based on their user ID.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        The HTTP status code is 201.
    """
    user = db_session.get(Users, user_id)
    item = request.args.get("item")
    if user and item:
        if item == "drop":
            user.passhash = generate_password_hash(
                current_app.config["DEFAULT_PASSWORD"]
            )
            user.attempt = 0
            user.blocked = False
            user.change_pswd = True
        elif item == "block":
            user.blocked = not user.blocked
        elif item == "delete":
            user.deleted = not user.deleted
        elif item in [reg.value for reg in Roles]:
            user.role = item
        elif item in [reg.value for reg in Regions]:
            user.region = item
        get_current_user.cache_clear()
        db_session.commit()
    return "", 201


@bp.get("/index/<int:page>")
@jwt_required()
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
    pagination = 1#0
    search_data = request.args.get("search")
    stmt = select(Persons, Users.fullname)
    if search_data and len(search_data) > 2:
        query = list(map(str.upper, search_data.split(maxsplit=2)))
        if len(query):
            stmt = stmt.filter(Persons.surname.ilike(f"%{query[0]}%"))
        if len(query) > 1:
            stmt = stmt.filter(Persons.firstname.ilike(f"%{query[1]}%"))
        if len(query) > 2:
            stmt = stmt.filter(Persons.patronymic.ilike(f"%{query[2]}%"))
    if current_user.get("region") != Regions.main.value:
        stmt = stmt.filter(Persons.region == current_user.get("region"))
    query = db_session.execute(
        stmt.filter(Persons.user_id == Users.id)
        .order_by(desc(Persons.id))
        .offset((page - 1) * pagination)
        .limit(pagination + 1)
    ).all()
    result = [row[0].to_dict() | {"username": row[1]} for row in query]
    has_next = len(result) > pagination
    result = result[:pagination] if has_next else result
    return jsonify([result, has_next, page > 1])


@bp.post("/file/<item>/<int:item_id>")
@roles_required(Roles.user.value)
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
    files = request.files.getlist("file")
    if not files:
        return abort(400)

    person = db_session.get(Persons, item_id)
    if not person:
        return abort(400)
    if person.destination and not os.path.isdir(person.destination):
        os.mkdir(person.destination)
    if not person.destination:
        person.destination = make_destination(
            current_user.get("region"),
            person.surname,
            person.firstname,
            person.patronymic,
            person.id,
        )
        db_session.commit()

    item_dir = os.path.join(person.destination, item)
    if not os.path.isdir(item_dir):
        os.mkdir(item_dir)

    if item == "image":
        handle_image(files[0], item_dir)
        return "", 201

    date_subfolder = os.path.join(
        item_dir,
        datetime.now().strftime("%Y-%m-%d"),
    )
    if not os.path.isdir(date_subfolder):
        os.mkdir(date_subfolder)
    for file in files:
        file_path = os.path.join(date_subfolder, file.filename)
        if not os.path.isfile(file_path):
            file.save(file_path)
    return "", 201


@bp.get("/folder")
@jwt_required()
def get_folder():
    """
    Opens a folder in the default file manager.

    Parameters:
        folder (str): The path to the folder to open.

    Returns:
        None

    Raises:
        None
    """
    folder = request.args.get("folder")
    if folder and not os.path.isdir(folder):
        os.mkdir(folder)
    if not folder:
        return abort(400)
    subprocess.run(f'explorer "{folder}"')
    # subprocess.run(["xdg-open", folder_path])
    return "", 200


@bp.get("/image")
def get_image():
    """
    Get a photo of the person.

    Args:
        image: path to the folder of the person

    Returns:
        photo of the person or a default no-photo image
    """
    image_path = request.args.get("image")
    if image_path:
        file_path = os.path.join(image_path, "image", "image.jpg")
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")


@bp.post("/json")
@roles_required(Roles.user.value)
def post_json():
    """
    Upload a json file with a person's data.

    Args:
        file: json file with a person's data.

    Returns:
        a json response with a person id, if the person was successfully added to the database.

    The json file should contain the following keys:
        - resume: a resume of a person
        - education: a list of education institutions of a person
        - work: a list of work places of a person
        - staff: a list of staff positions of a person
        - document: a list of documents of a person
        - address: a list of addresses of a person
    """
    file = request.files.get("file")
    if not file or not file.filename.endswith(".json"):
        return abort(400)
    json_dict = json.load(file)
    anketa = handle_json_to_dict(json_dict)
    if not anketa:
        return abort(400)
    person_id = handle_post_resume(anketa.pop("resume"))
    if not person_id:
        return abort(400)

    for table, contents in anketa.items():
        for content in contents:
            handle_post_item(content, table, person_id)
    return jsonify({"person_id": person_id}), 201


@bp.post("/resume")
@roles_required(Roles.user.value)
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
    resume = Person(**json_data).dict()
    person_id = handle_post_resume(resume)
    if not person_id:
        return abort(400)
    return jsonify({"person_id": person_id}), 201


@bp.get("/region/<int:person_id>")
@roles_required(Roles.user.value)
def change_region(person_id):
    """
    Change a person's region in the database based on their person ID.

    Parameters:
        person_id (int): The ID of the person.

    Returns:
        The HTTP status code is 200.
    """
    region = request.args.get("region")
    if region in [region.value for region in Regions]:
        person = db_session.get(Persons, person_id)
        if person.destination:
            destination = make_destination(
                region, person.surname, person.firstname, person.patronymic, person.id
            )
            shutil.move(person.destination, destination)
            person.destination = destination
        person.region = region
        person.editable = False
        db_session.commit()
    return "", 200


@bp.get("/self/<int:item_id>")
@roles_required(Roles.user.value)
def change_self_id(item_id):
    """
    Toggle the editable status of a person with the given item ID.

    The person ID is the ID of the person to toggle the editable status.
    The user ID is the ID of the user currently logged in.

    Returns:
        The HTTP status code is 200.
    """
    person = db_session.get(Persons, item_id)
    person.editable = not person.editable
    person.user_id = current_user.get("id")
    db_session.commit()
    return "", 200


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
    result = handle_get_item(item, item_id)
    return jsonify(result)


@bp.post("/<item>/<int:item_id>")
@roles_required(Roles.user.value)
def post_item_id(item, item_id):
    """
    Inserts or replaces a record in the specified table with the given item ID.

    Parameters:
        item (str): The name of the table to insert or replace the record in.
        item_id (int): The ID of the record to insert or replace.

    Returns:
        Tuple[str, int]: A tuple containing an empty string and an HTTP status
        code of 201.
    """
    json_data = request.get_json()
    handle_post_item(json_data, item, item_id)
    return "", 201


@bp.delete("/<item>/<int:item_id>")
@roles_required(Roles.user.value)
def delete_item(item, item_id):
    """
    Deletes an item from the database based on the provided item name and item ID.

    Parameters:
        item (str): The name of the table to delete the item from.
        item_id (int): The ID of the item to delete.

    Returns:
        Tuple[str, int]: A tuple containing an empty string and an HTTP status
        code of 204.
    """
    table = tables_models.get(item)
    if table:
        item = db_session.get(table, item_id)
        db_session.delete(item)
        db_session.commit()
    return "", 204


@bp.get("/information")
@jwt_required()
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
    results = db_session.execute(
        select(Checks.conclusion, func.count(Checks.id))
        .where(
            Checks.person_id == Persons.id,
            Checks.created.between(data["start"], data["end"]),
            Persons.region == data.get("region")
            if data.get("region")
            else current_user.get("region"),
        )
        .group_by(Checks.conclusion)
    ).all()
    return jsonify(
        [{"conclusion": result[0], "count": result[1]} for result in results]
    )
