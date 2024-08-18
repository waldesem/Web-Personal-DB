from datetime import datetime
import json
import os
import re
import shutil

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
)
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
from ..depends.depend import login_required, roles_required
from ..classes.classes import Roles
from ..model.models import Person, User, models_tables
from ..model.tables import Checks, Persons, Users, db_session, tables_models
from ..handlers.handler import (
    handle_image,
    handle_json_to_dict,
    handle_get_item,
    handle_post_item,
    handle_post_resume,
    handle_xml,
    make_destination,
)

bp = Blueprint(
    "route", __name__, url_prefix="/api", static_folder=current_app.config["BASE_PATH"]
)


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
    user = db_session.execute(
        select(Users).where(Users.username == request.form.get("login"))
    ).scalar_one_or_none()
    if not user or user.blocked or user.deleted:
        flash("Неверные данные", "danger")
        return render_template("/login/login.html")

    if not check_password_hash(user.passhash, request.form["password"]):
        if user.attempt < 5:
            user.attempt += 1
        else:
            user.blocked = True
        db_session.commit()
        flash("Неверные данные", "danger")
        return render_template("/login/login.html")

    if action == "update":
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,16}$"
        if re.match(pattern, request.form["new_pswd"]):
            user.passhash = generate_password_hash(request.form["new_pswd"])
            user.change_pswd = False
            user.attempt = 0
            db_session.commit()
            flash("Пароль успешно изменен", "success")
            return render_template("/login/login.html")

        flash("Новый пароль не соответствует требованиям", "danger")
        return render_template("/login/login.html")

    delta_change = datetime.now() - user.pswd_create
    if not user.change_pswd and delta_change.days < 365:
        session["user"] = user.to_dict()
        user.attempt = 0
        db_session.commit()
        return redirect("/api/index/1")
    flash("Пароль устарел и должен быть сменен", "danger")
    return render_template("/login/password.html")


@bp.get("/logout")
def get_logout():
    session.clear()
    return redirect("/login/create")


@bp.get("/users")
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
    result = [user.to_dict() for user in users]
    return jsonify(result), 200


@bp.post("/users")
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
def get_user_actions(user_id):
    if session["user"]["id"] == user_id:
        return "", 205
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
        db_session.commit()
        return "", 201
    return abort(400)


@bp.get("/index/<int:page>")
@login_required()
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
    pagination = 12
    search_data = request.args.get("search")
    stmt = select(Persons, Users.fullname)
    if search_data and len(search_data) > 2:
        if search_data.isdigit():
            stmt.filter(Persons.inn.ilike("%" + search_data + "%"))
        else:
            pattern = r"^\d{2}\.\d{2}\.\d{4}$"
            query = list(map(str.upper, search_data.split()))
            if len(query):
                stmt = stmt.filter(Persons.surname.ilike(f"%{query[0]}%"))
            if len(query) > 1 and not re.match(pattern, query[1]):
                stmt = stmt.filter(Persons.firstname.ilike(f"%{query[1]}%"))
            if len(query) > 2 and not re.match(pattern, query[2]):
                stmt = stmt.filter(Persons.patronymic.ilike(f"%{query[2]}%"))
            if len(query) > 1 and re.match(pattern, query[-1]):
                stmt = stmt.filter(
                    Persons.birthday == datetime.strptime(query[-1], "%d.%m.%Y").date()
                )
    if session["user"]["region"] != Regions.main.value:
        stmt = stmt.filter(Persons.region == session["user"]["region"])
    query = db_session.execute(
        stmt.join(Users)
        .order_by(desc(Persons.id))
        .limit(pagination + 1)
        .offset((page - 1) * pagination)
    ).all()
    result = [row[0].to_dict() | {"username": row[1]} for row in query]
    has_next = len(result) > pagination
    result = result[:pagination] if has_next else result
    return render_template(
        "persons.html",
        candidates=result,
        has_next=has_next,
        has_prev=page > 1,
        page=page,
    ), 200


@bp.post("/file/<item>/<int:item_id>")
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
    if not files or not files[0].filename:
        flash("Файл не выбран", "danger"), 400
        return render_template("create.html")

    if item == "persons":
        for file in files:
            json_dict = json.load(file)
            anketa = handle_json_to_dict(json_dict)
            if not anketa:
                flash("Некорректные данные", "danger")
                return render_template("create.html")
            person_id = handle_post_resume(anketa["resume"])
            if not person_id:
                flash("Некорректные данные", "danger")
                return render_template("create.html")
            for table, contents in anketa.items():
                if contents and table != "resume":
                    for content in contents:
                        if content:
                            handle_post_item(content, table, person_id)
        return redirect("/api/index/1"), 201

    person = db_session.get(Persons, item_id)
    if not person:
        return abort(400)
    try:
        if not person.destination:
            destination = make_destination(
                session["user"]["id"],
                person.surname,
                person.firstname,
                person.patronymic,
                item_id,
            )
            person.destination = destination
            db_session.commit()
        if not os.path.isdir(person.destination):
            os.mkdir(person.destination)

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
            if item == "checks" and file.filename == "showresult.xml":
                handle_xml(file, item_id)
            file_path = os.path.join(date_subfolder, file.filename)
            if not os.path.isfile(file_path):
                file.save(file_path)
        return "", 201
    except OSError as e:
        print(e)
        return abort(400)


@bp.get("/image")
def get_image():
    image_path = request.args.get("image")
    if image_path:
        file_path = os.path.join(image_path, "image", "image.jpg")
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True, mimetype="image/jpg")
        return send_file(
            "static/no-photo.png", as_attachment=True, mimetype="image/jpg"
        )


@bp.get("/create")
def create_resume():
    return render_template("create.html")


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
    resume = Person(**request.form).dict()
    person_id = handle_post_resume(resume)
    if person_id:
        return redirect("/api/index/1")
    return abort(400)


@bp.get("/region/<int:person_id>")
def change_region(person_id):
    """
    Change a person's region in the database based on their person ID.

    Parameters:
        person_id (int): The ID of the person.

    Returns:
        The HTTP status code is 200.
    """
    region = request.args.get("region")
    if region:
        person = db_session.get(Persons, person_id)
        if person.destination:
            destination = make_destination(
                region, person.surname, person.firstname, person.patronymic, person.id
            )
            shutil.move(person.destination, destination)
            person.destination = destination
        person.region = region
        person.standing = False
        db_session.commit()
        return "", 201
    return abort(400)


@bp.get("/profile/<int:person_id>")
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
    result = {item: handle_get_item(item, person_id) for item in tables_models.keys()}
    return jsonify(result), 200


@bp.get("/<item>/<int:item_id>")
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
        person.user_id = session["user"]["id"]
        db_session.commit()
    result = handle_get_item(item, item_id)
    return jsonify(result), 200


@bp.post("/<item>/<int:item_id>")
def post_item_id(item, item_id):
    """
    Inserts or replaces a record in the specified table with the given item ID.

    Parameters:
        item (str): The name of the table to insert or replace the record in.
        item_id (int): The ID of the record to insert or replace.

    Returns:
        Tuple[str, int]: A tuple containing an empty string and an HTTP status
        code of 201 if the operation is successful,
        otherwise a string containing the exception message and an HTTP status code of 400.
    """
    json_data = request.get_json()
    json_dict = models_tables[item](**json_data).dict()
    handle_post_item(json_dict, item, item_id)
    return "", 201


@bp.get("/delete/<item>/<int:item_id>")
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


@bp.get("/information")
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
        .join(Persons, Checks.person_id == Persons.id)
        .filter(
            Checks.created.between(data["start"], data["end"]),
            Persons.region == data.get("region")
            if data.get("region")
            else session["user"]["region"],
        )
        .group_by(Checks.conclusion)
    ).all()
    return jsonify([list(result) for result in results]), 200


@bp.get("/classes")
def get_classes():
    """
    Retrieves classes information and returns a JSON response.

    Returns:
        A JSON response containing information about Regions, Conclusions, Relations, Affiliates, Educations, Addresses, Contacts, Documents, and Poligrafs.
    """
    results = {
        items.__name__.lower(): {item.name: item.value for item in items}
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
            Roles,
        ]
    }
    return jsonify(results), 200
