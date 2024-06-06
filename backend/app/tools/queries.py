import sqlite3

from config import Config


def execute(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cursor = con.cursor()
        try:
            if isinstance(args, list):
                cursor.executemany(query, args)
            elif isinstance(args, tuple):
                cursor.execute(query, args)
            else:
                cursor.execute(query)
            con.commit()
            if "INSERT" in query:
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()


def execute_script(query):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cursor = con.cursor()
        try:
            cursor.executescript(query)
            con.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()


def select_all(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cursor = con.cursor()
        try:
            if isinstance(args, tuple):
                cursor.execute(query, args)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            if result:
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, res)) for res in result]
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()


def select_single(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI) as con:
        cursor = con.cursor()
        try:
            if isinstance(args, tuple):
                cursor.execute(query, args)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            if result:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            else:
                return None
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()
