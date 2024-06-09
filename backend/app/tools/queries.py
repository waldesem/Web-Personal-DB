import sqlite3

from config import Config


def execute(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cursor = con.cursor()
        try:
            result = cursor.execute(query, args)
            con.commit()
            return result.lastrowid if "INSERT" in query else None
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()


def execute_script(query):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cursor = con.cursor()
        cursor.executescript(query)
        con.commit()


def select_all(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cursor = con.cursor()
        try:
            if args is None:
                result = cursor.execute(query)
            else:
                result = cursor.execute(query, args)
            if result:
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, res)) for res in result.fetchall()]
            return []
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()


def select_single(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cursor = con.cursor()
        try:
            if args is None:
                result = cursor.execute(query).fetchone()
            else:
                result = cursor.execute(query, args).fetchone()
            columns = [desc[0] for desc in cursor.description] if result else []
            return dict(zip(columns, result)) if result else None
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()
