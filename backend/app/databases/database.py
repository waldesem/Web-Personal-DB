import sqlite3

from config import Config


def execute(query, args=None):
    with sqlite3.connect(Config.DATABASE_URI, timeout=1) as con:
        cursor = con.cursor()
        try:
            if isinstance(args, list):
                cursor.executemany(query, args)
            else:
                if args:
                    result = cursor.execute(query, args)
                else:
                    result = cursor.execute(query)
                con.commit()
                return result.lastrowid if "INSERT" in query else None
        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()


def select(query, many=False, args=None):
    with sqlite3.connect(Config.DATABASE_URI, timeout=1) as con:
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

        except sqlite3.Error as e:
            print(f"Error: {e}")
            con.rollback()
