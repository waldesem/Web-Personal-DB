import sqlite3

from config import Config


def execute(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        try:
            con.execute(query, args or ())
            lastrowid = (
                con.execute("SELECT last_insert_rowid()").fetchone()[0]
                if "INSERT" in query
                else None
            )
            con.commit()
            return lastrowid
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()


def execute_script(query):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        con.executescript(query)
        con.commit()


def select_all(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        try:
            if args is None:
                result = con.execute(query)
            else:
                result = con.execute(query, args)
            return [dict(row) for row in result.fetchall()]
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()


def select_single(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        try:
            if args is None:
                result = con.execute(query).fetchone()
            else:
                result = con.execute(query, args).fetchone()
            return dict(zip(*result)) if result else None
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()
