import imghdr
import os
import re
import shutil

from flask import abort, current_app
from PIL import Image
from pydantic import ValidationError
from sqlalchemy import desc, select

from ..depends.depend import current_user
from ..model.models import Person, models_tables
from ..model.tables import Users, db_session, Persons, tables_models


def handle_get_item(item, item_id):
    """
    Retrieves an item from the database based on the provided item and item_id.

    Args:
        item (str): The type of item to retrieve.
        item_id (int): The ID of the item to retrieve.

    Returns:
        dict or list: If item is "persons", a dictionary containing the item's data and the associated user's fullname.
                      Otherwise, a list of dictionaries containing the item's data and the associated user's fullname,
                      ordered by descending item ID.
    Raises:
        None
    """
    table = tables_models.get(item)
    if table:
        stmt = select(table, Users.fullname)
        stmt = (
            stmt.filter(Persons.id == item_id)
            if item == "persons"
            else stmt.filter(table.person_id == item_id)
        )
        stmt = stmt.filter(table.user_id == Users.id)
        query = db_session.execute(stmt.order_by(desc(table.id))).all()
        result = [row[0].to_dict() | {"username": row[1]} for row in query]
        return result[0] if item == "persons" else result
    return abort(400)


def handle_post_item(data: dict, item: str, item_id=None):
    """
    Updates an item in the database based on the provided JSON data, item, and item_id.

    Args:
        data (dict): A dictionary containing the data to update the item.
        item (str): The type of item to update in the database.
        item_id (int): The ID of the item to update.

    Returns:
        None
    """
    table, model = tables_models.get(item), models_tables.get(item)
    if model and table:
        try:
            data = model(**data).dict()
        except ValidationError as e:
            print(e)
            return False
        if item != "persons":
            data["person_id"] = item_id
        data["user_id"] = current_user.get("id")
        db_session.merge(table(**data))
        db_session.commit()
        return True
    return False


def handle_post_resume(resume: dict):
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
        resume = Person(**resume).dict()
    except ValidationError:
        return None
    if not re.match(r"[А-ЯЁЙ]", resume["surname"][0]):
        return None
    resume["editable"] = True
    resume["user_id"] = current_user.get("id")
    resume["region"] = current_user.get("region")
    person = db_session.execute(
        select(Persons).where(
            Persons.surname.ilike("%{}%".format(resume["surname"])),
            Persons.firstname.ilike("%{}%".format(resume["firstname"])),
            Persons.patronymic.ilike("%{}%".format(resume["patronymic"])),
            Persons.birthday == resume["birthday"],
        )
    ).scalar_one_or_none()
    if not person:
        person = Persons(**resume)
        db_session.add(person)
        db_session.flush()
        person.destination = make_destination(
            resume["region"],
            resume["surname"],
            resume["firstname"],
            resume.get("patronymic", ""),
            person.id,
        )
        db_session.commit()
        return person.id

    if person.editable:
        return None

    destination = make_destination(
        resume["region"],
        resume["surname"],
        resume["firstname"],
        resume.get("patronymic", ""),
        person.id,
    )
    if person.destination and not os.path.isdir(person.destination):
        os.mkdir(person.destination)
    if person.destination and resume["region"] != person.region:
        shutil.move(person.destination, destination)
    resume.update({"destination": destination, "id": person.id})
    return resume["id"] if handle_post_item(resume, "persons") else None


def json_to_dict(json_dict: dict):
    return {
        "resume": {
            "region": current_user.get("region"),
            "surname": json_dict.get("lastName"),
            "firstname": json_dict.get("firstName"),
            "patronymic": json_dict.get("midName"),
            "birthday": json_dict.get("birthday"),
            "birthplace": json_dict.get("birthplace"),
            "citizenship": json_dict.get("citizen", ""),
            "dual": json_dict.get("additionalCitizenship"),
            "marital": json_dict.get("maritalStatus"),
            "inn": json_dict.get("inn"),
            "snils": json_dict.get("snils"),
        },
        "staffs": [
            {
                "position": json_dict.get("positionName"),
                "department": json_dict.get("department"),
            }
        ],
        "documents": [
            {
                "view": "Паспорт",
                "digits": json_dict.get("passportNumber"),
                "series": json_dict.get("passportSerial"),
                "issue": json_dict.get("passportIssueDate"),
                "agency": json_dict.get("passportIssuedBy"),
            }
        ],
        "addresses": [
            {
                "view": "Адрес проживания",
                "addresses": json_dict.get("validAddress"),
            },
            {
                "view": "Адрес регистрации",
                "addresses": json_dict.get("regAddress"),
            },
        ],
        "contacts": [
            {"view": "Телефон", "contact": json_dict.get("contactPhone")},
            {"view": "Электронная почта", "contact": json_dict.get("email")},
        ],
        "educations": [
            {
                "view": edu.get("educationType"),
                "institution": edu.get("institutionName"),
                "finished": edu.get("endYear"),
                "specialty": edu.get("specialty"),
            }
            for edu in json_dict.get("education")
            if json_dict.get("education")
        ],
        "workplaces": [
            {
                "starts": work.get("beginDate"),
                "finished": work.get("endDate"),
                "now_work": work.get("currentJob"),
                "workplace": work.get("name"),
                "addresses": work.get("address"),
                "reason": work.get("fireReason"),
                "position": work.get("position"),
            }
            for work in json_dict.get("experience")
            if json_dict.get("experience")
        ],
        "previous": [
            {
                "firstname": prev.get("firstNameBeforeChange"),
                "surname": prev.get("lastNameBeforeChange"),
                "patronymic": prev.get("midNameBeforeChange"),
                "changed": prev.get("yearOfChange"),
                "reason": prev.get("reason"),
            }
            for prev in json_dict.get("nameWasChanged")
            if json_dict.get("nameWasChanged")
        ],
        "affilations": (
            [
                {
                    "view": "Участвует в деятельности коммерческих организаций",
                    "organization": aff.get("name"),
                    "inn": aff.get("inn"),
                }
                for aff in json_dict.get("organizations")
                if json_dict.get("organizations")
            ]
            + [
                {
                    "view": "Являлся государственным должностным лицом",
                    "organization": aff.get("name"),
                }
                for aff in json_dict.get("stateOrganizations")
                if json_dict.get("stateOrganizations")
            ]
            + [
                {
                    "view": "Связанные лица работают в государственных организациях",
                    "organization": aff.get("name"),
                }
                for aff in json_dict.get("relatedPersonsOrganizations")
                if json_dict.get("relatedPersonsOrganizations")
            ]
            + [
                {
                    "view": "Являлся государственным или муниципальным служащим",
                    "organization": aff.get("name"),
                }
                for aff in json_dict.get("publicOfficeOrganizations")
                if json_dict.get("publicOfficeOrganizations")
            ]
        ),
    }


def handle_image(file, item_dir):
    """
    Opens a file, reads the image data, saves it to a new file in a specified directory.

    Args:
        file (str): The path to the file containing the image.
        item_dir (str): The directory where the new image file will be saved.

    Returns:
        None
    """
    if imghdr.what(file) is not None:
        image = Image.open(file)
        image = image.convert("RGB")
        new_file = os.path.join(item_dir, "image.jpg")
        if os.path.isfile(new_file):
            os.remove(new_file)
        image.save(new_file, format="JPEG", quality=90)
        return True
    return False


def make_destination(region, surname, firstname, patronymic, person_id):
    """
    Generate the destination directory path for a given set of parameters.

    Args:
        region (str): The region of the destination directory.
        surname (str): The surname of the person.
        firstname (str): The firstname of the person.
        patronymic (str): The patronymic of the person.
        person_id (str): The unique identifier of the person.

    Returns:
        str: The full path of the destination directory.

    Raises:
        None
    """
    destination = os.path.join(
        current_app.config["BASE_PATH"],
        region,
        surname[0],
        f"{person_id}-{surname} {firstname} "
        f"{patronymic if patronymic else ''}".rstrip().upper(),
    )
    if not os.path.isdir(destination):
        os.mkdir(destination)
    return destination
