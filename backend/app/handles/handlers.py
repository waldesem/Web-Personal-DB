import os

from flask import current_app 

from ..classes.classes import Statuses
from ..databases.database import execute, select
from ..depends.depend import current_user
from ..models.models import Person
from ..tools.jsonylize import parse_json


def handle_get_person(person_id):
    result = select(
        """
        SELECT persons.*, users.fullname AS username 
        FROM persons
        LEFT JOIN users ON persons.user_id = users.id 
        WHERE persons.id = ?""",
        args=(person_id,),
    )
    return result


def handle_get_item(item, item_id):
    if item in ["checks", "poligrafs", "inquiries", "investigations"]:
        stmt = f"SELECT {item}.*, users.fullname AS user FROM {item} LEFT JOIN users ON {item}.user_id = users.id "
    else:
        stmt = f"SELECT * FROM {item} "
    result = select(
        stmt + "WHERE person_id = ? ORDER BY id ASC", many=True, args=(item_id,)
    )
    return result


def handle_post_resume(data):
    """
    Updates a resume in the database with the provided data.

    Args:
        data (dict): A dictionary containing the resume data.

    Returns:
        int: The ID of the updated resume.

    Raises:
        Exception: If there is an error updating the resume.

    """
    try:
        resume = Person(**data).dict()
        if not resume["id"]:
            stmt = """
                SELECT * FROM persons 
                WHERE surname LIKE '%{}%' 
                AND firstname LIKE '%{}%' 
                AND patronymic LIKE '%{}%'
                AND birthday = ?
                """.format(resume["surname"], resume["firstname"], resume["patronymic"])
            person = select(stmt, args=(resume["birthday"],))
            if person:
                resume["id"] = person["id"]

            resume["standing"] = Statuses.manual.value
            resume["user_id"] = current_user["id"]
            
        keys, args = zip(*resume.items())
        stmt = "INSERT OR REPLACE INTO persons ({}) VALUES ({})".format(
            ", ".join(keys),
            ", ".join(["?" for _ in keys]),
        )
        person_id = execute(stmt, args)

        person_dir = os.path.join(
            current_app.config["BASE_PATH"],
            resume["region"],
            resume["surname"][0].upper(),
            f"{person_id}-{resume['surname'].upper()} "
            f"{resume['firstname'].upper()} "
            f"{resume.get('patronymic', '').upper()}".rstrip(),
        )
        if not os.path.isdir(person_dir):
            os.mkdir(person_dir)

        execute(
            "UPDATE persons SET destination = ? WHERE id = ?",
            (
                person_dir,
                person_id,
            ),
        )
        return person_id
    except Exception as e:
        print(e)
        return None


def handle_update_person(json_data):
    """
    Updates a person's information in the database.

    Args:
        json_data (str): The JSON data containing the person's information.

    Returns:
        int: The ID of the updated person.

    Raises:
        Exception: If there is an error updating the person's information.

    """
    anketa = parse_json(json_data)
    person_id = None
    if anketa:
        person_id = handle_post_resume(anketa["resume"])
        if person_id:
            for table, contents in anketa.items():
                if table == "resume" or not contents:
                    continue
                keys = list(contents[0].keys()) + ["person_id"]
                args = [tuple(list(cont.values()) + [person_id]) for cont in contents]
                stmt = f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join(['?' for _ in keys])})"
                execute(stmt, args)
    return person_id
