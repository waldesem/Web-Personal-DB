import os

from flask import current_app
from pydantic import ValidationError
from sqlalchemy import desc, select

from ..depends.depend import current_user
from ..model.models import AnketaSchemaJson
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


def handle_post_resume(resume):
    """
    Updates a resume in the database with the provided data.

    Args:
        data (dict): A dictionary containing the resume data.

    Returns:
        int: The ID of the updated resume.

    Raises:
        Exception: If there is an error updating the resume.

    """
    resume["standing"] = True
    resume["user_id"] = current_user["id"]
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
            if person.user_id != current_user["id"]:
                return None
            resume["id"] = person.id
            for k, v in resume.items():
                setattr(person, k, v)
            db_session.commit()
            return resume["id"]
    handle_post_item(resume, "persons")
    return resume["id"]


def handle_post_item(json_dict, item, item_id = ""):
    """
    Updates an item in the database based on the provided JSON data, item, and item_id.

    Args:
        json_data (dict): A dictionary containing the data to update the item.
        item (str): The type of item to update in the database.
        item_id (int): The ID of the item to update.

    Returns:
        None
    """
    if item != "persons":
        json_dict["person_id"] = item_id
        json_dict["user_id"] = current_user["id"]
    db_session.merge(tables_models[item](**json_dict))
    db_session.commit()


def handle_json_to_dict(data):
    try:
        anketa = AnketaSchemaJson(**data).dict()
        anketa["resume"] = {
            "region": current_user["region"],
            "surname": anketa.pop("surname", "").upper(),
            "firstname": anketa.pop("firstname", "").upper(),
            "patronymic": anketa.pop("patronymic", "").upper(),
            "birthday": anketa.pop("birthday", ""),
            "birthplace": anketa.pop("birthplace", ""),
            "citizenship": anketa.pop("citizenship", ""),
            "dual": anketa.pop("dual", ""),
            "marital": anketa.pop("marital", ""),
            "inn": anketa.pop("inn", ""),
            "snils": anketa.pop("snils", ""),
        }
        anketa["staffs"].append(
            {
                "position": anketa.pop("positionName", ""),
                "department": anketa.pop("department", ""),
            }
        )
        anketa["documents"].append(
            {
                "view": "Паспорт",
                "digits": anketa.pop("passportNumber", ""),
                "series": anketa.pop("passportSerial", ""),
                "issue": anketa.pop("passportIssueDate", ""),
                "agency": anketa.pop("passportIssuedBy", ""),
            }
        )
        anketa["addresses"].extend(
            [
                {
                    "view": "Адрес проживания",
                    "addresses": anketa.pop("validAddress", ""),
                },
                {
                    "view": "Адрес регистрации",
                    "addresses": anketa.pop("regAddress", ""),
                },
            ]
        )
        anketa["contacts"].extend(
            [
                {"view": "Телефон", "contact": anketa.pop("contactPhone", "")},
                {"view": "Электронная почта", "contact": anketa.pop("email", "")},
            ]
        )
        anketa["affilations"].extend(
            anketa.pop("organizations")
            + anketa.pop("stateOrganizations")
            + anketa.pop("publicOfficeOrganizations")
            + anketa.pop("relatedPersonsOrganizations")
        )
        return anketa
    except ValidationError as e:
        print(e)
        return None


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
