import sqlite3

from config import Config


def select_from_table(exec, select, args=""):
    with sqlite3.connect(Config.DATABASE_URI) as conn:
        cursor = conn.cursor()
        query = cursor.execute(select, args)
        col_names = [q[0] for q in query.description]
        if exec == "fetchall":
            return [dict(zip(col_names, q)) for q in query.fetchall()]
        else:
            return dict(zip(col_names, query.fetchone()))