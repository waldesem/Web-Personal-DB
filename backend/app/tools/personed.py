from datetime import datetime
import re

from ..classes.classes import Statuses, Regions
from ..databases.database import execute
from ..depends.depend import current_user
from ..models.models import Person
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


def get_region_id(json_dict):
    """
    Retrieves the region ID from a given JSON dictionary.

    Args:
        json_dict (dict): The JSON dictionary to extract the region ID from.

    Returns:
        str: The region ID.

    """
    region = Regions.main.value
    if "department" in json_dict and json_dict.get("department"):
        for reg in [r for r in Regions]:
            if reg.value.upper() in re.split(r"/", json_dict["department"].upper()):
                region = reg.value
                break
    return region


def parse_json(json_dict: dict) -> dict:
    json_data = {
        "resume": {
            "region": get_region_id(json_dict),
            "firstname": json_dict["firstName"],
            "surname": json_dict["lastName"],
            "patronymic": json_dict.get("midName"),
            "birthday": datetime.strptime(json_dict["birthday"], "%Y-%m-%d").date(),
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
                "address": json_dict.get("validAddress"),
            },
            {
                "view": "Адрес регистрации",
                "address": json_dict.get("regAddress"),
            },
        ],
        "contacts": [
            {"view": "Телефон", "contact": json_dict.get("contactPhone")},
            {"view": "Электронная почта", "contact": json_dict.get("email")},
        ],
        "documents": [
            {
                "view": "Паспорт гражданина России",
                "number": json_dict.get("passportNumber"),
                "series": json_dict.get("passportSerial"),
                "issue": datetime.strptime(
                    json_dict["passportIssueDate"], "%Y-%m-%d"
                ).date()
                if json_dict.get("passportIssueDate")
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
        "previous": [],
        "educations": [],
        "workplaces": [],
        "affilations": [],
    }
    for item, values in json_dict.items():
        if values:
            views = {
                "publicOfficeOrganizations": "Являлся государственным или муниципальным служащим",
                "stateOrganizations": "Являлся государственным должностным лицом",
                "relatedPersonsOrganizations": "Связанные лица работают в госудраственных организациях",
                "organizations": "Участвует в деятельности коммерческих организаций",
            }
            if item in views.keys():
                for org in values:
                    organization = {}
                    organization["view"] = views[item]
                    for k, v in org.items():
                        match k:
                            case "name":
                                org["name"] = v
                            case "position":
                                org["position"] = v
                            case "inn":
                                org["inn"] = v
                    json_data["affilations"].append(organization)

            elif item == "previous":
                for prev in values:
                    previous = {}
                    for k, v in prev.items():
                        match k:
                            case "firstNameBeforeChange":
                                previous["firstname"] = k
                            case "lastNameBeforeChange":
                                previous["surname"] = k
                            case "midNameBeforeChange":
                                previous["patronymic"] = k
                            case "yearOfChange":
                                previous["changed"] = k
                            case "reason":
                                previous["reason"] = v
                    json_data["previous"].append(previous)

            elif item == "education":
                for edu in values:
                    education = {}
                    for k, v in edu.items():
                        match k:
                            case "educationType":
                                education["view"] = v
                            case "institutionName":
                                education["name"] = v
                            case "endYear":
                                education["finished"] = v
                            case "speciality":
                                education["specialty"] = v
                    json_data["educations"].append(education)

            elif item == "experience":
                for exp in values:
                    work = {}
                    for key, value in exp.items():
                        match key:
                            case "beginDate":
                                work["started"] = datetime.strptime(
                                    value, "%Y-%m-%d"
                                ).date()
                            case "endDate":
                                work["finished"] = datetime.strptime(
                                    value, "%Y-%m-%d"
                                ).date()
                            case "currentJob":
                                work["now_work"] = bool(value)
                            case "name":
                                work["workplace"] = value
                            case "address":
                                work["address"] = value
                            case "position":
                                work["position"] = value
                            case "fireReason":
                                work["reason"] = value
                    json_data["workplaces"].append(work)
    return json_data
