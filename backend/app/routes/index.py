from datetime import datetime
import os
import re

from flask import jsonify, request, send_file

from . import bp
from config import Config
from ..tools.folders import Folders
from ..tools.depends import current_user, jwt_required, user_required
from ..tools.queries import select_all, select_single
from ..tools.classes import Conclusions, Regions, Statuses, Relations


@bp.route("/index/<flag>/<int:page>")
@user_required()
def get_index(flag, page):
    """
    Retrieves a paginated list of persons based on the given flag and page number.

    Args:
        flag (str): The type of search to perform. Can be "search" or "officer".
        page (int): The page number to retrieve.

    Returns:
        A JSON response containing the list of persons and pagination information.
    """
    # Construct SQL query based on flag
    stmt = "SELECT * FROM persons "

    # Perform search based on flag
    if flag == "search":
        # Retrieve search data from request arguments
        search_data = request.args.get("search", "")
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
                if current_user["region"] != Regions.main.name:
                    stmt += "AND region = {} ".format(current_user["region"])
        else:
            if current_user["region"] != Regions.main.name:
                stmt += "WHERE region = {} ".format(current_user["region"])
    if flag == "officer":
        stmt += "WHERE status = {} AND user_id = {} ".format(
            Statuses.manual.name, current_user["id"]
        )

    # Add sorting and pagination to SQL query
    stmt += "ORDER BY {} {} LIMIT {} OFFSET {}".format(
        request.args.get("sort"),
        request.args.get("order"),
        Config.PAGINATION + 1,
        (page - 1) * Config.PAGINATION,
    )

    # Execute SQL query and retrieve result
    result = select_all(stmt)

    # Check if there are more pages
    has_next = len(result) > Config.PAGINATION if result else False

    # Truncate result if there are more pages
    result = result[: Config.PAGINATION] if has_next else result

    # Retrieve user names for each person
    users = select_all("SELECT id, fullname FROM users")
    names = {u["id"]: u["fullname"] for u in users}

    # Add username to each person if user_id exists
    if result:
        for i in result:
            if i["user_id"]:
                i["username"] = names[i["user_id"]]

    # Return JSON response with result and pagination information
    return jsonify(
        {
            "persons": result,
            "has_next": has_next,
            "has_prev": page > 1,
        }
    ), 200


@bp.route("/information")
@jwt_required()
def get_information():
    """
    Retrieves information about the checks performed in a given region and date range.

    Returns:
        A JSON response containing the number of checks for each conclusion.
    """
    # Get the query parameters from the request
    query_data = request.args

    # Execute the database query to retrieve the information
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

    # Return the result as a JSON response
    return jsonify(result), 200


@bp.route("/image/<int:item_id>")
@jwt_required()
def get_image(item_id):
    """
    Retrieves a file from the server and sends it as a response.

    Args:
        item_id (int): The ID of the item for which to retrieve the image.

    Returns:
        A response containing the image file if it exists, or a default image file if it does not.
    """
    # Retrieve the person information from the database
    person = select_single("SELECT * FROM persons WHERE id = ?", (item_id,))

    # Create a Folders object with the person's information
    folders = Folders(
        person["id"],
        person["surname"],
        person["firstname"],
        person.get("patronymic", ""),
    )

    # Construct the file path to the image file
    file_path = os.path.join(folders.create_main_folder(), "image", "image.jpg")

    # Check if the image file exists
    if os.path.isfile(file_path):
        # If it does, send the file as a response
        return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    else:
        # If it does not, send the default image file as a response
        return send_file(
            "static/no-photo.png", as_attachment=True, mimetype="image/jpg"
        )


@bp.get("/classes")
def get_classes():
    """
    Retrieves all classes with their corresponding values and returns them as a JSON response.

    Returns:
        A JSON response containing the classes and their values.
    """
    # Retrieve all classes with their corresponding values
    results = [
        {item.name: item.value for item in items}  # Convert each class to a dictionary
        for items in [
            Regions,
            Statuses,
            Conclusions,
            Relations,
        ]  # Iterate over each class
    ]

    # Return the results as a JSON response
    return jsonify(results), 200
