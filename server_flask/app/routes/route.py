import imghdr
import json
import os
import re
import shutil
import subprocess
from datetime import datetime

from flask import Blueprint, current_app, jsonify, request, send_file
from pydantic import ValidationError
from PIL import Image
from sqlalchemy import desc, func, select
from werkzeug.security import check_password_hash, generate_password_hash

from ..depends.depend import (
    create_token,
    current_user,
    get_current_user,
    get_payload,
    jwt_required,
    roles_required,
)
from ..model.classes import Regions, Roles
from ..model.models import AnketaSchemaJson, Login, Model, Person, Relation, User
from ..model.tables import Base, Checks, Persons, Users, association_table, db_session
from ..utils.utils import json_to_dict

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
    try:
        json_data = Login(**json_data).dict()
    except ValidationError as e:
        current_app.logger.exception(e)
        return {"message": "Denied"}
    user = db_session.execute(
        select(Users).filter(
            func.lower(Users.username) == json_data["username"].lower()
        )
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
        user.attempt = 0
        db_session.commit()
        token = create_token(User(**user.to_dict()).dict())
        if token:
            return jsonify(
                {
                    "message": "Success",
                    "user_token": token,
                }
            )
    return {"message": "Denied"}


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
            stmt = stmt.filter(Users.username.like(f"{search_data}%"))
        else:
            stmt = stmt.filter(Users.fullname.like(f"{search_data}%"))
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
        returns an empty response with status code 200.
    """
    json_dict = request.get_json()
    try:
        json_dict = User(**json_dict).dict()
    except ValidationError as e:
        current_app.logger.exception(e)
        return jsonify({"message": "error"}), 204
    user = db_session.execute(
        select(Users).filter(Users.username == json_dict["username"])
    ).all()
    if not user:
        json_dict["role"] = Roles.guest.value
        json_dict["region"] = Regions.main.value
        json_dict["passhash"] = generate_password_hash(
            current_app.config["DEFAULT_PASSWORD"]
        )
        db_session.add(Users(**json_dict))
        db_session.commit()
        return jsonify({"message": "success"}), 201
    return jsonify({"message": "error"}), 200


@bp.get("/users/<int:user_id>")
@roles_required(Roles.admin.value)
def get_user_actions(user_id):
    """
    Change a user's information in the database based on their user ID.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        The HTTP status code is 201.
    """
    if current_user.get("id") == user_id:
        return jsonify({"message": "error"}), 200
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
        db_session.commit()
        get_current_user.cache_clear()
        get_payload.cache_clear()
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
    pagination = 11
    search_data = request.args.get("search", "")
    stmt = select(Persons, Users.fullname).filter(
        Persons.user_id == Users.id,
        Persons.region == current_user.get("region")
        if current_user.get("region") != Regions.main.value
        else True,
    )
    if len(search_data) > 2:
        search = search_data.upper().split()[:3]
        stmt = stmt.filter(
            Persons.surname = search[0],
            Persons.firstname = search[1] if len(query) > 1 else True,
            Persons.patronymic = search[2] if len(query) > 2 else True,
        )
    query = db_session.execute(
        stmt.order_by(desc(Persons.editable), desc(Persons.id))
        .offset((page - 1) * pagination)
        .limit(pagination + 1)
    ).all()
    result = [row[0].to_dict() | {"username": row[1]} for row in query]
    has_next = len(result) > pagination
    result = result[:pagination] if has_next else result
    return jsonify([result, has_next])


@bp.route("/file/<item>/<int:item_id>", methods=["GET", "POST"])
@roles_required(Roles.user.value)
def use_filesystem(item, item_id):
    """
    Handles the GET and POST requests for the file system.

    Args:
        item (str): The name of the item.
        item_id (int): The ID of the person.

    Returns:
        Response: A Flask Response object containing the image file.

    Raises:
        None.
    """

    person = db_session.get(Persons, item_id)
    if not person.destination or not os.path.isdir(person.destination):
        person.destination = os.path.join(
            current_app.config["BASE_PATH"],
            current_user.get("region"),
            person.surname[0],
            f"{person.id}-{person.surname} {person.firstname} "
            f"{person.patronymic if person.patronymic else ''}".rstrip().upper(),
        )
        os.makedirs(person.destination, exist_ok=True)
        db_session.commit()

    if request.method == "GET":
        if item == "folder":
            try:
                subprocess.run(f'explorer "{person.destination}"', timeout=10)
            except subprocess.CalledProcessError as e:
                current_app.logger.exception(e)
            return "", 200
        elif item == "image":
            file_path = os.path.join(person.destination, "image", "image.jpg")
            if os.path.isfile(file_path):
                return send_file(file_path, as_attachment=True, mimetype="image/jpg")
            return send_file(
                "static/no-photo.png", as_attachment=True, mimetype="image/jpg"
            )

    else:
        item_dir = os.path.join(person.destination, item)
        os.makedirs(item_dir, exist_ok=True)

        files = request.files.getlist("file")
        if not files:
            return jsonify({"message": "error"}), 200

        if item == "image":
            if imghdr.what(files[0]) is not None:
                image = Image.open(files[0])
                image = image.convert("RGB")
                new_file = os.path.join(item_dir, "image.jpg")
                if os.path.isfile(new_file):
                    os.remove(new_file)
                image.save(new_file, format="JPEG", quality=90)
                return jsonify({"message": "success"}), 201
            return jsonify({"message": "error"}), 200

        date_subfolder = os.path.join(
            item_dir,
            datetime.now().strftime("%Y-%m-%d"),
        )
        os.makedirs(date_subfolder, exist_ok=True)
        for file in files:
            file_path = os.path.join(date_subfolder, file.filename)
            if not os.path.isfile(file_path):
                file.save(file_path)
        return "", 201


@bp.post("/anketa/<item>")
@roles_required(Roles.user.value)
def post_resume(item):
    """
    Creates a new person or updates an existing person based on the provided data.

    Parameters:
        item (str): The name to create or update the person in.

    Returns:
        A JSON response containing the person ID and an HTTP status code of 201.
    """

    def upload_resume(resume: dict):
        try:
            resume = Person(**resume).dict()
        except ValidationError as e:
            current_app.logger.exception(e)
            return None
        if not re.match(r"[А-ЯЁЙ]", resume["surname"][0]):
            return None
        resume["editable"] = True
        resume["user_id"] = current_user.get("id")
        resume["region"] = current_user.get("region")
        person = db_session.execute(
            select(Persons).where(
                Persons.surname == resume["surname"],
                Persons.firstname == resume["firstname"],
                Persons.patronymic == resume["patronymic"],
                Persons.birthday == resume["birthday"],
            )
        ).scalar_one_or_none()

        if not person:
            person = Persons(**resume)
            db_session.add(person)
            db_session.flush()
            person.destination = os.path.join(
                current_app.config["BASE_PATH"],
                resume["region"],
                resume["surname"][0],
                f"{person.id}-{resume['surname']} {resume['firstname']} "
                f"{resume.get('patronymic', '')}".rstrip().upper(),
            )
            if not os.path.isdir(person.destination):
                os.mkdir(person.destination)
            db_session.commit()
            return person.id

        if person.editable or resume["region"] != person.region:
            return None

        resume["id"] = person.id
        db_session.merge(Persons(**resume))
        db_session.commit()
        return person.id

    if item == "resume":
        json_data = request.get_json()
        person_id = upload_resume(json_data) if json_data else None
        return jsonify({"person_id": person_id})

    else:
        file = request.files.get("file")
        if not file or not file.filename.endswith(".json"):
            return jsonify({"person_id": None})
        json_dict = json.load(file)
        try:
            json_dict = AnketaSchemaJson(**json_dict).dict()
        except ValidationError as e:
            current_app.logger.exception(e)
            return jsonify({"person_id": None})

        anketa = json_to_dict(json_dict)
        person_id = upload_resume(anketa.pop("resume"))
        if not person_id:
            current_app.logger.warning("person_id is None")
            return jsonify({"person_id": person_id})

        tables = {
            cls.__tablename__: cls
            for cls in Base.__subclasses__()
            if hasattr(cls, "__tablename__")
        }
        items = []
        for tbl, contents in anketa.items():
            if contents:
                for content in contents:
                    content["person_id"] = person_id
                    content["user_id"] = current_user.get("id")
                    table = tables.get(tbl)
                    items.append(table(**content))
        db_session.bulk_save_objects(items)
        db_session.commit()
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
    person = db_session.get(Persons, person_id)
    if region in [region.value for region in Regions] and region != person.region:
        if person.destination and os.path.isdir(person.destination):
            destination = os.path.join(
                current_app.config["BASE_PATH"],
                region,
                person.surname[0],
                f"{person_id}-{person.surname} {person.firstname} "
                f"{person.patronymic if person.patronymic else ''}".rstrip().upper(),
            )
            shutil.copytree(person.destination, destination, dirs_exist_ok=True)
            person.destination = destination
        person.region = region
        person.editable = False
        db_session.commit()
        return jsonify({"message": "success"}), 201
    return jsonify({"message": "error"}), 200


@bp.get("/self/<int:person_id>")
@roles_required(Roles.user.value)
def change_self_id(person_id):
    """
    Toggle the editable status of a person with the given item ID.

    The person ID is the ID of the person to toggle the editable status.
    The user ID is the ID of the user currently logged in.

    Returns:
        The HTTP status code is 200.
    """
    person = db_session.get(Persons, person_id)
    person.editable = not person.editable
    person.user_id = current_user.get("id")
    db_session.commit()
    return "", 200


@bp.get("/items/<item>/<int:item_id>")
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
    if item == "persons":
        person = db_session.get(Persons, item_id)
        if not person:
            return "", 404
        return jsonify(person.to_dict()), 200
    else:
        table = Base.metadata.tables.get(item)
        stmt = table.select().filter(table.c.person_id == item_id)
        query = db_session.execute(stmt.order_by(desc(table.c.id)))
        return jsonify([row._asdict() for row in query])


@bp.post("/items/<item>/<int:item_id>")
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
    models = {
        cls.__modelname__: cls
        for cls in Model.__subclasses__()
        if hasattr(cls, "__modelname__")
    }
    table, model = Base.metadata.tables.get(item), models.get(item)
    try:
        json_data = model(**json_data).dict()
    except ValidationError as e:
        current_app.logger.exception(e)
        return jsonify({"message": "error"}), 200
    if item != "persons":
        json_data["person_id"] = item_id
    json_data["user_id"] = current_user.get("id")
    table_id = json_data.pop("id", None)
    stmt = (
        table.update().where(table.c.id == table_id).values(json_data)
        if table_id
        else table.insert().values(json_data)
    )
    db_session.execute(stmt)
    db_session.commit()
    return jsonify({"message": "success"}), 201


@bp.delete("/items/<item>/<int:item_id>")
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
    tables = Base.metadata.tables
    table = tables.get(item)
    if item == "persons":
        for model, tbl in tables.items():
            if model not in ["users", "persons", "person_relationships"]:
                db_session.execute(tbl.delete().where(tbl.c.person_id == item_id))
        db_session.execute(
            association_table.delete().where(association_table.c.left_id == item_id)
        )
        db_session.execute(
            association_table.delete().where(association_table.c.right_id == item_id)
        )
    db_session.execute(table.delete().where(table.c.id == item_id))
    db_session.commit()
    return jsonify({"message": "success"}), 201


@bp.get("/relations/<int:person_id>")
@roles_required(Roles.user.value)
def get_relation(person_id):
    """
    Retrieves a person's relationships from the database based on their person ID.

    Parameters:
        person_id (int): The ID of the person.

    Returns:
        Tuple[Response, int]: A tuple containing the JSON response containing
        the retrieved person's relationships and an HTTP status code of 200.
    """
    relation = db_session.execute(
        association_table.select().where(association_table.c.left_id == person_id)
    )
    relationship = db_session.execute(
        association_table.select().where(association_table.c.right_id == person_id)
    )
    return jsonify(
        [
            [i._asdict() for i in relation],
            [i._asdict() for i in relationship],
        ]
    ), 200


@bp.post("/relations/<int:person_id>")
@roles_required(Roles.user.value)
def post_relation(person_id):
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
    try:
        json_data = Relation(**json_data).dict()
    except ValidationError:
        return jsonify({"message": "error"}), 200
    if json_data["right_id"] != person_id and db_session.get(
        Persons, json_data["right_id"]
    ):
        relationship = association_table.insert().values(
            left_id=person_id,
            right_id=json_data["right_id"],
            type=json_data["type"],
        )
        db_session.execute(relationship)
        db_session.commit()
        return jsonify({"message": "success"}), 201
    return jsonify({"message": "error"}), 200


@bp.delete("/relations/<int:person_id>/<int:relation_id>")
@roles_required(Roles.user.value)
def delete_relation(person_id, relation_id):
    """
    Deletes an item from the database based on the provided item name and item ID.

    Parameters:
        item (str): The name of the table to delete the item from.
        item_id (int): The ID of the item to delete.

    Returns:
        Tuple[str, int]: A tuple containing an empty string and an HTTP status
        code of 204.
    """
    person = db_session.get(Persons, person_id)
    related_person = db_session.get(Persons, relation_id)
    person.relationships.remove(related_person)
    db_session.commit()
    return jsonify({"message": "success"}), 201


@bp.get("/info")
@jwt_required()
def get_information():
    """
    Retrieves information based on the provided query parameters.

    Returns:
        A JSON response containing the count of checks for each conclusion within the specified date range and region.
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
