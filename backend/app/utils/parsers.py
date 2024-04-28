import re
import os
import shutil

from sqlalchemy import select

from ..utils.folders import Folders
from ..routes.resume import add_resume
from ..models.classes import Statuses
from ..models.model import (
    db,
    Previous,
    Education,
    Staff,
    Document,
    Address,
    Contact,
    Workplace,
    Affilation,
    Person,
    Region,
    Status,
)


def parse_json(json_dict) -> None:
    json_data = {
        "resume": {
            "status_id": Status().get_id(Statuses.new.name),
            "region_id": get_region_id(json_dict),
            "firstname": json_dict["firstName"].strip().upper(),
            "surname": json_dict["lastName"].strip().upper(),
            "birthday": json_dict["birthday"],
            "birthplace": json_dict["birthplace"].strip(),
            "citizen": json_dict["citizen"].strip(),
        },
        "previous": json_dict["nameWasChanged"],
        "education": json_dict["education"],
        "workplace": json_dict["experience"],
        "address": [],
        "contact": [],
        "document": [],
        "affilation": [],
        "staff": [
            {
                "position": json_dict.get("positionName").strip(),
                "department": json_dict.get("department").strip(),
            }
        ],
    }
    for item in json_dict:
        match item:
            case "midName":
                json_data["patronymic"] = json_dict["midName"].strip().upper()
            case "additionalCitizenship":
                json_data["ext_country"] = json_dict["additionalCitizenship"]
            case "maritalStatus":
                json_data["marital"] = json_dict["maritalStatus"]
            case "inn":
                json_data["inn"] = json_dict["inn"].strip()
            case "snils":
                json_data["snils"] = json_dict["snils"].strip()
            case "ValidAddress":
                json_data["address"].append(
                    {"view": "Адрес проживания", "address": json_dict["ValidAddress"]}
                )
            case "RegAddress":
                json_data["address"].append(
                    {"view": "Адрес регистрации", "address": json_dict["RegAddress"]}
                )
            case "contactPhone":
                json_data["contact"].append(
                    {"view": "Телефон", "phone": json_dict["contactPhone"]}
                )
            case "email":
                json_data["contact"].append(
                    {"view": "Электронная почта", "email": json_dict["email"]}
                )
            case "passportNumber":
                json_data["document"].append(
                    {
                        "view": "Паспорт",
                        "number": json_dict["passportNumber"].strip(),
                        "series": json_dict.get("passportSerial").strip(),
                        "issue": json_dict.get("passportIssueDate"),
                        "agency": json_dict.get("passportIssuedBy"),
                    }
                )
            case "organization":
                json_data["affilation"] + json_dict["organization"]
            case "relatedPersonsOrganizations":
                json_data["affilation"] + json_dict["relatedPersonsOrganizations"]
            case "publicOfficeOrganizations":
                json_data["affilation"] + json_dict["publicOfficeOrganizations"]
            case "stateOrganizations":
                json_data["affilation"] + json_dict["stateOrganizations"]

    return json_data


def get_region_id(json_dict):
    region_id = 1
    if "department" in json_dict:
        divisions = re.split(r"/", json_dict["department"].strip())
        for div in divisions:
            region = Region().get_id(div)
            if region:
                region_id = region
    return region_id


def add_resume(resume: dict):
    """
    Adds a resume to the database.
    """
    person = db.session.execute(
        select(Person).filter(
            Person.surname.ilike(resume["surname"]),
            Person.firstname.ilike(resume["firstname"]),
            Person.patronymic.ilike(resume.get("patronymic")),
            Person.birthday == resume["birthday"],
        )
    ).one_or_none()

    for k, v in resume.items():
        if k in ["surname", "firstname", "patronymic"]:
            resume[k] = v.strip().upper()

    if person:
        person_id = person.id
        for k, v in resume.items():
            setattr(person, k, v)
    else:
        resume["status_id"] = Status().get_id(Statuses.new.value)
        person = Person(**resume)
        db.session.add(person)
        db.session.flush()
        person_id = person.id

    folsers = Folders(
        person_id,
        resume["surname"],
        resume["firstname"],
        resume.get("patronymic", ""),
    )
    person.path = folsers.create_main_folder()
    db.session.commit()
    return person_id


def parse_anketa(anketa):
    person_id = None
    if len(anketa["previous"]):
        prev_id = []
        for item in anketa["previous"]:
            prev = db.session.execute(
                select(Person).filter(
                    Person.surname.ilike(
                        item.get("surname") 
                        if item.get("surname") 
                        else anketa["resume"]["surname"]
                    ),
                    Person.firstname.ilike(
                        item.get("firstname")
                        if item.get("firstname")
                        else anketa["resume"]["firstname"]
                    ),
                    Person.patronymic.ilike(
                        item.get("patronymic")
                        if item.get("patronymic")
                        else anketa["resume"].get("patronymic")
                    ),
                    Person.birthday == anketa["resume"]["birthday"],
                )
            ).one_or_none()
            if prev:
                prev_id.append(prev.id)

        if prev_id:
            person_id = max(prev_id)
            previous = db.session.get(Previous, person_id)

            if previous.path:
                folders = Folders(person_id, previous.surname, previous.firstname, previous.patronymic)
                new_path = folders.create_main_folder()
                shutil.copytree(previous.path, new_path)
                os.remove(previous.path)
                previous.path = new_path
                
            for k, v in anketa["resume"].items():
                setattr(previous, k, v)

            addition = f"Кандидат ранее проверялся ID: {', '.join(prev_id)}"
            previous.addition = (
                previous.addition + "\n " + addition 
                if previous.addition 
                else addition
                    )
            db.session.commit()
    
    if not person_id:
        person_id = add_resume(anketa["resume"])

    models = [
        Previous,
        Education,
        Staff,
        Document,
        Address,
        Contact,
        Workplace,
        Affilation,
    ]
    items_lists = [
        anketa["previous"],
        anketa["education"],
        anketa["staff"],
        anketa["document"],
        anketa["address"],
        anketa["contact"],
        anketa["workplace"],
        anketa["affilation"],
    ]
    for model, items in zip(models, items_lists):
        for item in items:
            if item:
                db.session.add(model(**item | {"person_id": person_id}))

    
    db.session.commit()

    return person_id
