from ..classes.classes import Statuses
from ..databases.database import execute, select
from ..depends.depend import current_user
from ..models.models import Person
from ..tools.tool import Folders, parse_json


def handle_get_person(person_id):
    return select(
        """
        SELECT persons.*, users.fullname AS username 
        FROM persons
        LEFT JOIN users ON persons.user_id = users.id 
        WHERE persons.id = ?""",
        args=(person_id,),
    )


def handle_get_item(item, item_id):
    if item in ["checks", "poligrafs", "inquiries", "investigations"]:
        stmt = f"SELECT {item}.*, users.fullname AS user FROM {item} LEFT JOIN users ON {item}.user_id = users.id "
    else:
        stmt = f"SELECT * FROM {item} "
    return select(
        stmt + "WHERE person_id = ? ORDER BY id DESC", many=True, args=(item_id,)
    )


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

    try:
        resume.update({"standing": Statuses.manual.value, "user_id": current_user["id"]})
        keys, args = zip(*resume.items())
        stmt = "INSERT OR REPLACE INTO persons ({}) VALUES ({})".format(
            ", ".join(keys),
            ", ".join(["?" for _ in keys]),
        )
        person_id = execute(stmt, args)
        folders = Folders(
            resume["region"],
            person_id,
            resume["surname"],
            resume["firstname"],
            resume.get("patronymic", ""),
        )
        path = folders.create_main_folder()
        execute(
            "UPDATE persons SET path = ? WHERE id = ?",
            (
                path,
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
            for table, values in anketa.items():
                if table == "resume":
                    continue 
                keys = []
                args = []
                for item in values:
                    item["person_id"] = person_id
                    keys, arg = zip(*item.items())
                    args.append(tuple(arg))

                stmt = f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join(['?' for _ in keys])})"
                execute(stmt, args=args, many=True)
    return person_id
