from ..classes.classes import Statuses
from ..databases.database import execute
from ..depends.depend import current_user
from ..models.models import Person
from .jsoned import parse_json
from .foldered import Folders


def update_resume(data):
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
    try:
        resume['status'] = Statuses.manual.value
        resume['user_id'] = current_user["id"]
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


def update_person(json_data):
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
    person_id = update_resume(anketa["resume"])
    for table, values in anketa.items():
        if table == "resume":
            continue
        for item in values:
            item["person_id"] = person_id
            keys, args = zip(*item.items())
            stmt = f"INSERT INTO {table} ({','.join(keys)}) VALUES ({','.join(['?' for _ in keys])})"
            execute(stmt, tuple(args))
    return person_id
