import sqlite3

from config import Config


def execute(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI, timeout=1) as con:
        cursor = con.cursor()
        try:
            if isinstance(args, list):
                cursor.executemany(query, args)
            else:
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
    with sqlite3.connect(Config.DATABASE_URI, timeout=1) as con:
        cursor = con.cursor()
        try:
            if args is None:
                cursor.execute(query)
            else:
                cursor.execute(query, args)
            result = cursor.fetchall()
            if result:
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, res)) for res in result]
            return []
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()


def select_single(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI, timeout=1) as con:
        cursor = con.cursor()
        try:
            if args is None:
                cursor.execute(query)
            else:
                cursor.execute(query, args)
            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            return None
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()
