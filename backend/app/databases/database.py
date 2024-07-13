import sqlite3

import psycopg2

from flask import current_app


def connect_to_database():
    connection = (
        sqlite3.connect(current_app.config["SQLITE_URI"])
        if "sqlite" in current_app.config["DATABASE_URI"]
        else psycopg2.connect(current_app.config["POSTGRE_URI"])
    )
    return connection


def execute(query, args=None):
    """
    Executes a SQL query on the database using the provided query and arguments.

    Args:
        query (str): The SQL query to execute.
        args (Optional[list]): The arguments to pass to the query. Defaults to None.

    Returns:
        Union[int, None]: The last inserted row ID if the query is an INSERT statement, None otherwise.

    Raises:
        sqlite3.Error: If an error occurs while executing the query.

    """
    with connect_to_database() as con:
        cursor = con.cursor()
        try:
            if isinstance(args, list):
                cursor.executemany(query, args)
            else:
                result = cursor.execute(query, args) if args else cursor.execute(query)
                con.commit()
                return result.lastrowid
        except con.Error as e:
            print(f"Error: {e}")
            con.rollback()
            return "Error"


def select(query, many=False, args=None):
    """
    Executes a SQL query on the database using the provided query and arguments.

    Args:
        query (str): The SQL query to execute.
        many (bool, optional): Whether to fetch multiple rows. Defaults to False.
        args (Optional[list], optional): The arguments to pass to the query. Defaults to None.

    Returns:
        Union[list, dict, None]: A list of dictionaries if `many` is True, a dictionary if `many` is False,
        and None if no rows are returned.

    Raises:
        sqlite3.Error: If an error occurs while executing the query.

    """
    with connect_to_database() as con:
        cursor = con.cursor()
        try:
            cursor.execute(query, args) if args else cursor.execute(query)
            result = cursor.fetchall() if many else cursor.fetchone()

            if result:
                columns = [desc[0] for desc in cursor.description]
                if many:
                    return [dict(zip(columns, res)) for res in result]
                return dict(zip(columns, result))

            return [] if many else None

        except con.Error as e:
            print(f"Error: {e}")
            con.rollback()
            return "Error"
