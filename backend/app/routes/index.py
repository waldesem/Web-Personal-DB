import re
from datetime import datetime

from config import Config
from flask import jsonify, request

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
from ..tools.depends import current_user, jwt_required, user_required
from ..tools.queries import select_all
from . import bp


@bp.route("/index/<int:page>")
@user_required()
def get_index(page):
    """
    Retrieves a paginated list of persons based on page number.

    Args:
        page (int): The page number to retrieve.

    Returns:
        A JSON response containing the list of persons and pagination information.
    """
    # Construct SQL query
    stmt = "SELECT * FROM persons "
    search_data = request.args.get("search", "")

    # Retrieve search data from request arguments
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
    return jsonify([result, has_next, page > 1]), 200


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
            Affiliates,
            Educations,
            Addresses,
            Contacts,
            Poligrafs,
            Documents,
        ]  # Iterate over each class
    ]

    # Return the results as a JSON response
    return jsonify(results), 200
