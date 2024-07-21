from datetime import datetime
import os
import re

from flask import current_app
from sqlalchemy import desc, select

from ..depends.depend import current_user
from ..model.models import Person, models_tables
from ..model.tables import Users, db_session, Persons, tables_models


def parse_json(json_dict: dict):
    """
    Parses a JSON dictionary and returns a dictionary with the parsed data.

    Args:
        json_dict (dict): The JSON dictionary to parse.

    Returns:
        dict: The parsed dictionary.
    """
    json_data = {
        "resume": {
            "region": current_user.region,
            "firstname": json_dict.get("firstName"),
            "surname": json_dict.get("lastName"),
            "patronymic": json_dict.get("midName"),
            "birthday": datetime.strptime(json_dict["birthday"], "%Y-%m-%d").date()
            if json_dict.get("birthday")
            and re.match(r"^\d{4}-\d{2}-\d{2}$", json_dict["birthday"])
            else None,
            "birthplace": json_dict.get("birthplace"),
            "citizenship": json_dict.get("citizen"),
            "dual": json_dict.get("additionalCitizenship"),
            "inn": json_dict.get("inn"),
            "snils": json_dict.get("snils"),
            "marital": json_dict.get("maritalStatus"),
        },
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
        "documents": [
            {
                "view": "Паспорт",
                "digits": json_dict.get("passportNumber"),
                "series": json_dict.get("passportSerial"),
                "issue": datetime.strptime(
                    json_dict["passportIssueDate"], "%Y-%m-%d"
                ).date()
                if json_dict.get("passportIssueDate")
                and re.match(r"^\d{4}-\d{2}-\d{2}$", json_dict["passportIssueDate"])
                else None,
                "agency": json_dict.get("passportIssuedBy"),
            }
        ],
        "staffs": [
            {
                "position": json_dict.get("positionName"),
                "department": json_dict.get("department"),
            }
        ],
        "previous": [
            {
                "firstname": prev.get("firstNameBeforeChange"),
                "surname": prev.get("lastNameBeforeChange"),
                "patronymic": prev.get("midNameBeforeChange"),
                "changed": prev.get("yearOfChange"),
                "reason": prev.get("reason"),
            }
            for prev in json_dict.get("nameWasChanged", [])
        ],
        "educations": [
            {
                "view": edu.get("educationType"),
                "institution": edu.get("institutionName"),
                "finished": edu.get("endYear"),
                "specialty": edu.get("specialty"),
            }
            for edu in json_dict.get("education", [])
        ],
        "workplaces": [
            {
                "starts": datetime.strptime(exp["beginDate"], "%Y-%m-%d").date()
                if exp.get("beginDate")
                and re.match(r"^\d{4}-\d{2}-\d{2}$", exp["beginDate"])
                else None,
                "finished": datetime.strptime(exp["endDate"], "%Y-%m-%d").date()
                if exp.get("endDate")
                and re.match(r"^\d{4}-\d{2}-\d{2}$", exp["endDate"])
                else None,
                "now_work": True if exp.get("currentJob") else False,
                "workplace": exp.get("name"),
                "addresses": exp.get("address"),
                "position": exp.get("position"),
                "reason": exp.get("fireReason"),
            }
            for exp in json_dict.get("experience", [])
        ],
        "affilations": [],
    }
    views = {
        "publicOfficeOrganizations": "Являлся государственным или муниципальным служащим",
        "stateOrganizations": "Являлся государственным должностным лицом",
        "relatedPersonsOrganizations": "Связанные лица работают в государственных организациях",
        "organizations": "Участвует в деятельности коммерческих организаций",
    }
    for item, value in views.items():
        affils = json_dict.get(item, [])
        for org in affils:
            json_data["affilations"].append(
                {
                    "view": value,
                    "organization": org.get("name"),
                    "position": org.get("position"),
                    "inn": org.get("inn"),
                }
            )

    return (
        json_data
        if json_data["resume"]["surname"]
        and json_data["resume"]["firstname"]
        and json_data["resume"]["birthday"]
        else None
    )


def make_destination(region, surname, firstname, patronymic, person_id):
    destination = os.path.join(
        current_app.config["BASE_PATH"],
        region,
        surname[0].upper(),
        f"{person_id}-{surname.upper()} "
        f"{firstname.upper()} "
        f"{patronymic.upper()}".rstrip(),
    )
    if not os.path.isdir(destination):
        os.mkdir(destination)
    return destination


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
    stmt = select(tables_models[item], Users.fullname).filter(
        tables_models[item].user_id == Users.id
    )
    if item == "persons":
        stmt = stmt.filter(Persons.id == item_id)
    else:
        stmt = stmt.filter(tables_models[item].person_id == item_id).order_by(
            desc(tables_models[item].id)
        )
    query = db_session.execute(stmt).all()
    result = [row[0].to_dict() | {"username": row[1]} for row in query]
    return result[0] if item == "persons" else result


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
    resume["standing"] = True
    resume["user_id"] = current_user.id
    if not resume.get("id"):
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
        else:
            if person.user_id != current_user.id:
                return None
            resume["id"] = person.id
    handle_post_item(resume, "persons", resume["id"])
    return resume["id"]


def handle_post_item(json_data, item, item_id):
    """
    Updates an item in the database based on the provided JSON data, item, and item_id.

    Args:
        json_data (dict): A dictionary containing the data to update the item.
        item (str): The type of item to update in the database.
        item_id (int): The ID of the item to update.

    Returns:
        None
    """
    json_dict = models_tables[item](**json_data).dict()
    if item != "persons":
        json_dict["person_id"] = item_id
    json_dict["user_id"] = current_user.id
    db_session.merge(tables_models[item](**json_dict))
    db_session.commit()
