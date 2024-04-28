import re
import os
from datetime import datetime

from sqlalchemy import select

from ..utils.folders import Folders
from ..utils.parsers import parse_json
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
    Status
)

def parse_json(json_dict) -> None:
    json_data = dict(
        resume = {},
        previous = [],
        education = [],
        address = [],
        contact = [],
        workplace = [],
        document = [],
        staff = [],
        affilation = [],
    )

    json_data["resume"]["status_id"] = Status().get_id(Statuses.new.name),
    for key, value in json_dict.items():
        match key:
            case "department":
                region_id = 1
                divisions = re.split(r"/", json_dict["department"].strip())
                for div in divisions:
                    region = Region().get_id(div)
                    if region:
                        region_id = region
                json_data["resume"]["region_id"] = region_id
            case "lastName":
                json_data["resume"]["surname"] = value.strip().upper()
            case "firstName":
                json_data["resume"]["firstname"] = value.strip().upper()
            case "midName":
                json_data["resume"]["patronymic"] = value.strip().upper()
            case "nameWasChanged":
                if len(json_dict["nameWasChanged"]):
                    for name in json_dict["nameWasChanged"]:
                        prev = {}
                        for key, value in name.items():
                            match key:
                                case "firstNameBeforeChange":
                                    prev["surname"] = value
                                case "lastNameBeforeChange":
                                    prev["firstName"] = value
                                case "midNameBeforeChange":
                                    prev["patronymic"] = value
                                case "yearOfChange":
                                    prev["date_change"] = value
                                case "reason":
                                    prev["reason"] = value
                        json_data["previous"].append(prev)
            case "birthday":
                json_data["resume"]["birthday"] = value
            case "birthplace":
                json_data["resume"]["birthplace"] = value
            case "citizen":
                json_data["resume"]["country"] = value
            case "ext_country":
                json_data["resume"]["ext_country"] = value
            case "snils":
                json_data["resume"]["snils"] = value
            case "inn":
                json_data["resume"]["inn"] = value
            case "maritalStatus":
                json_data["resume"]["marital"] = value
            case "education":
                json_data["education"].append(
                    {   
                        "type": item.get("educationType", ""),
                        "name": item.get("institutionName", ""),
                        "end": item.get("endYear", "н.в."),
                        "specialty": item.get("specialty", "")
                    }
                )
            case "passportNumber":
                json_data["document"].append(
                    {
                        "view": "Паспорт",
                        "number": value,
                        "series": json_dict.get("passportSerial", ""),
                        "issue": json_dict.get("passportIssueDate", ""),
                        "agency": json_dict.get("passportIssuedBy", ""),
                    }
                )
            case "regAddress":
                json_data["address"].append(
                    {"view": "Адрес регистрации", "address": value}
                )
            case "validAddress":
                json_data["address"].append(
                    {"view": "Адрес проживания", "address": value}
                )
            case "contactPhone":
                json_data["contact"].append({"view": "Телефон", "contact": value})
            case "email":
                json_data["contact"].append({"view": "E-mail", "contact": value})
            case "positionName":
                json_data["staff"].append(
                    {
                        "position": value,
                        "department": json_dict.get("department", ""),
                    }
                )
            case "experience":
                if len(json_dict["experience"]):
                    for exp in json_dict["experience"]:
                        work = {}
                        for key, value in exp.items():
                            match key:
                                case "beginDate":
                                    work["start_date"] = datetime.strptime(
                                        value, "%Y-%m-%d"
                                    )
                                case "endDate":
                                    work["end_date"] = datetime.strptime(
                                        value, "%Y-%m-%d"
                                    )
                                case "currentJob":
                                    work["now_work"] = True
                                case "name":
                                    work["workplace"] = value
                                case "address":
                                    work["address"] = value
                                case "position":
                                    work["position"] = value
                                case "fireReason":
                                    work["reason"] = value
                    json_data["workplace"].append(work)
            case "publicOfficeOrganizations":
                if len(json_dict["publicOfficeOrganizations"]):
                    for item in json_dict["publicOfficeOrganizations"]:
                        public = {
                            "view": "Являлся государственным или муниципальным служащим",
                            "name": f"{item.get('name', '')}",
                            "position": f"{item.get('position', '')}",
                        }
                        json_data["affilation"].append(public)

            case "stateOrganizations":
                if len(json_dict["stateOrganizations"]):
                    for item in json_dict["stateOrganizations"]:
                        state = {
                            "view": "Являлся государственным должностным лицом",
                            "name": f"{item.get('name', '')}",
                            "position": f"{item.get('position', '')}",
                        }
                        json_data["affilation"].append(state)

            case "relatedPersonsOrganizations":
                if len(json_dict["relatedPersonsOrganizations"]):
                    for item in json_dict["relatedPersonsOrganizations"]:
                        related = {
                            "view": "Связанные лица работают в госудраственных организациях",
                            "name": f"{item.get('name', '')}",
                            "position": f"{item.get('position', '')}",
                            "inn": f"{item.get('inn'), ''}",
                        }
                        json_data["affilation"].append(related)

            case "organizations":
                if len(json_dict["organizations"]):
                    for item in json_dict["organizations"]:
                        organization = {
                            "view": 'Участвует в деятельности коммерческих организаций"',
                            "name": f"{item.get('name', '')}",
                            "position": f"{item.get('workCombinationTime', '')}",
                            "inn": f"{item.get('inn'), ''}",
                        }
                        json_data["affilation"].append(organization)  
    return json_data



def parse_anketa(json_dict):
    anketa = parse_json(json_dict)
    person_id = add_resume(anketa["resume"])

    person = db.session.get(Person, person_id)
    if person.path:
        if not os.path.isdir(person.path):
            os.mkdir(person.path)
    else:
        folders = Folders(
            person_id, person.surname, person.firstname, person.patronymic
        )
        person.path = folders.create_main_folder()
    models = [
        Previous, Education, Staff, Document, Address, Contact, Workplace, Affilation
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
    check_previous(anketa, person_id)

    return person_id


def check_previous(anketa, person_id):
    additional = ""
    if len(anketa["previous"]):
        for item in anketa["previous"]:
            surname = item["surname"] if item.get("surname") else anketa["surname"]
            firstname = (
                item["firstname"] if item.get("firstname") else anketa["firstname"]
            )
            patronymic = (
                item["patronymic"] if item.get("patronymic") else anketa["patronymic"]
            )

            result = db.session.execute(
                select(Person).filter(
                    Person.surname.ilike(surname),
                    Person.firstname.ilike(firstname),
                    Person.patronymic.ilike(patronymic),
                    Person.birthday == anketa["birthday"],
                )
            ).one_or_none()

            if result:
                message = (
                    f"Кандидат {anketa.surname} ID: {anketa.id} "
                    f"ранее проверялся как {result.surname} ID: {result.id}"
                )
                additional = additional + "\n " + message
    person = db.session.get(Person, person_id)
    person.addition = (
        person.addition + "\n " + additional if person.addition else additional
    )
    db.session.commit()
