import sqlite3

from flask import jsonify, request

from . import bp
from config import Config
from ..models.models import Connects
from ..tools.depends import jwt_required
from ..tools.queries import select_all, execute


@bp.route("/connectors")
def get_connectors():
    # Retrieve names, companies, and cities from the database
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        cur = conn.cursor()
        cur.execute("SELECT view, company, city FROM connects")
        result = cur.fetchall()
        view, company, city = [], [], []
        if result:
            view, company, city = zip(*result)
        # Return the results as a JSON response
        return jsonify(
            {
                "view": list(set(view)),
                "companies": list(set(company)),
                "cities": list(set(city)),
            }
        )


@bp.get("/connect/<int:page>")
@jwt_required()
def get_connects(page):
    """
    Retrieves a paginated list of Connect objects based on the specified group and item.

    Args:
        page (int): The page number of the results.

    Returns:
        Flask Response: The JSON response containing the paginated list of contacts,
                        whether there is a next page, whether there is a previous page.
    """
    # Get the search query from the request arguments
    search_data = request.args.get("search", "")

    # Calculate the offset and limit for the SQL query
    offset = (page - 1) * Config.PAGINATION
    limit = Config.PAGINATION + 1

    # Construct the SQL query
    query = "SELECT * FROM connects "
    if search_data:
        # Add the search condition to the query
        query += "WHERE company LIKE '%{}%' ".format(search_data.upper())
    query += "ORDER BY id DESC LIMIT ? OFFSET ?"

    # Execute the SQL query and retrieve the results
    result = select_all(query, (limit, offset,))

    # Check if there is a next page
    has_next = len(result) > Config.PAGINATION

    # Truncate the results if there is a next page
    result = result[:Config.PAGINATION] if has_next else result

    # Construct the response JSON
    response = {
        "contacts": result,
        "has_next": has_next,
        "has_prev": page > 1,
    }

    # Return the JSON response with a 200 status code
    return jsonify(response), 200


@bp.post("/connect")
@jwt_required()
def post_connect():
    """
    Create or update connection.

    This endpoint accepts a JSON payload containing the data for the
    connection. The payload should be a dictionary with the keys being the
    column names of the 'connects' table and the values being the values for
    those columns.

    Returns:
        A tuple containing an empty string and a status code of 201 on success.
        If an exception occurs, a tuple containing the error message and a
        status code of 400 is returned.
    """
    # Get the JSON payload from the request
    json_data = request.get_json()

    try:
        # Convert the JSON payload to a dictionary and remove any keys that
        # are not in the 'connects' table
        json_dict = Connects(**json_data).dict()

        # Generate the SQL query and arguments for inserting the new connection
        keys, args = zip(*json_dict.items())
        query = "INSERT OR REPLACE INTO connects ({}) VALUES ({})".format(
            ",".join(keys),
            ",".join("?" for _ in keys)
        )

        # Execute the SQL query
        execute(query, args)

        # Return a success response
        return "", 201

    except Exception as e:
        # Return an error response if an exception occurs
        print(str(e))
        return "", 400


@bp.delete("/connect/<int:item_id>")
@jwt_required()
def delete(item_id):
    """
    Delete an item from the database.

    Args:
        item_id (int): The ID of the item to delete.

    Returns:
        tuple: A tuple containing an empty string and a status code of 204 on
                success.
    """
    # Execute the SQL query to delete the item from the database
    execute("DELETE FROM connects WHERE id = ?", (item_id,))

    # Return a success response with a status code of 204
    return "", 204
