import re
import json
from datetime import datetime

from ..models.model import Region, Status, Category
from ..models.classes import Statuses, Categories


def parse_json(file) -> None:
    with open(file, "r", newline="", encoding="utf-8-sig") as f:
        json_dict = json.load(f)
        person = {}

        person.update(
            {
                "resume": {
                    "region_id": parse_region(json_dict),
                    "category_id": Category().get_id(Categories.candidate.name),
                    "status_id": Status().get_id(Statuses.new.name),
                    "fullname": parse_fullname(),
                    "previous": parse_previous(),
                    "birthday": parse_birthday(),
                    "birthplace": json_dict.get("birthplace", "").strip(),
                    "country": json_dict.get("citizen" "").strip(),
                    "ext_country": json_dict.get("additionalCitizenship", "").strip(),
                    "snils": json_dict.get("snils", "").strip(),
                    "inn": json_dict.get("inn", "").strip(),
                    "marital": json_dict.get("maritalStatus", "").strip(),
                    "education": parse_education(),
                }
            }
        )

        person.update({"workplaces": parse_workplace()})

        person.update(
            {
                "passport": [
                    {
                        "view": "Паспорт",
                        "series": json_dict.get("passportSerial", "").strip(),
                        "number": json_dict.get("passportNumber", "").strip(),
                        "issue": datetime.strptime(
                            json_dict.get("passportIssueDate", "1900-01-01"),
                            "%Y-%m-%d",
                        ),
                        "agency": json_dict.get("passportIssuedBy", "").strip(),
                    }
                ]
            }
        )
        person.update(
            {
                "addresses": [
                    {
                        "view": "Адрес регистрации",
                        "address": json_dict.get("regAddress", "").strip(),
                    },
                    {
                        "view": "Адрес проживания",
                        "address": json_dict.get("validAddress", "").strip(),
                    },
                ]
            }
        )
        person.update(
            {
                "contacts": [
                    {
                        "view": "Мобильный телефон",
                        "contact": json_dict.get("contactPhone", "").strip(),
                    },
                    {
                        "view": "Электронная почта",
                        "contact": json_dict.get("email", "").strip(),
                    },
                ]
            }
        )
        person.update(
            {
                "staff": [
                    {
                        "position": json_dict.get("positionName", "").strip(),
                        "department": json_dict.get("department", "").strip(),
                    }
                ]
            }
        )
        person.update({"affilation": parse_affilation()})

        return person

def parse_region(json_dict):
    if "department" in json_dict:
        divisions = re.split(r"/", json_dict["department"].strip())
        for div in divisions:
            region_id = Region().get_id(div)
            if region_id:
                return region_id
            else:
                return 1


def parse_fullname(json_dict):
    lastName = json_dict.get("lastName").strip()
    firstName = json_dict.get("firstName").strip()
    midName = json_dict.get("midName", "").strip()
    return f"{lastName} {firstName} {midName}".rstrip().upper()


def parse_birthday(json_dict):
    birthday = datetime.strptime(json_dict.get("birthday", "1900-01-01"), "%Y-%m-%d")
    return birthday


def parse_previous(json_dict):
    if "hasNameChanged" in json_dict:
        if len(json_dict["nameWasChanged"]):
            previous = []
            for item in json_dict["nameWasChanged"]:
                firstNameBeforeChange = item.get("firstNameBeforeChange", "").strip()
                lastNameBeforeChange = item.get("lastNameBeforeChange", "").strip()
                midNameBeforeChange = item.get("midNameBeforeChange", "").strip()
                yearOfChange = str(item.get("yearOfChange", "")).strip()
                reason = str(item.get("reason", "")).strip()
                previous.append(
                    f"{yearOfChange} - {firstNameBeforeChange} "
                    f"{lastNameBeforeChange} {midNameBeforeChange}, "
                    f"{reason}".replace("  ", "")
                )
            return "; ".join(previous)
    return ""


def parse_education(json_dict):
    if "education" in json_dict:
        if len(json_dict["education"]):
            education = []
            for item in json_dict["education"]:
                institutionName = item.get("institutionName").strip()
                endYear = item.get("endYear", "н.в.")
                specialty = item.get("specialty").strip()
                education.append(
                    f"{str(endYear)} - {institutionName}, "
                    f"{specialty}".replace("  ", "")
                )
            return "; ".join(education)
    return ""


def parse_workplace(json_dict):
    if "experience" in json_dict:
        if len(json_dict["experience"]):
            experience = []
            for item in json_dict["experience"]:
                work = {
                    "start_date": datetime.strptime(
                        item.get("beginDate", "1900-01-01"), "%Y-%m-%d"
                    ),
                    "end_date": (
                        datetime.strptime(item["endDate"], "%Y-%m-%d")
                        if "endDate" in item
                        else datetime.now()
                    ),
                    "workplace": item.get("name", "").strip(),
                    "address": item.get("address", "").strip(),
                    "position": item.get("position", "").strip(),
                    "reason": item.get("fireReason", "").strip(),
                }
                experience.append(work)
            return experience
    return []


def parse_affilation(json_dict):
    affilation = []
    if json_dict["hasPublicOfficeOrganizations"]:
        if len(json_dict["publicOfficeOrganizations"]):
            for item in json_dict["publicOfficeOrganizations"]:
                public = {
                    "view": "Являлся государственным или муниципальным служащим",
                    "name": f"{item.get('name', '')}",
                    "position": f"{item.get('position', '')}",
                }
                affilation.append(public)

    if json_dict["hasStateOrganizations"]:
        if len(json_dict["stateOrganizations"]):
            for item in json_dict["publicOfficeOrganizations"]:
                state = {
                    "view": "Являлся государственным должностным лицом",
                    "name": f"{item.get('name', '')}",
                    "position": f"{item.get('position', '')}",
                }
                affilation.append(state)

    if json_dict["hasRelatedPersonsOrganizations"]:
        if len(json_dict["relatedPersonsOrganizations"]):
            for item in json_dict["relatedPersonsOrganizations"]:
                related = {
                    "view": "Связанные лица работают в госудраственных организациях",
                    "name": f"{item.get('name', '')}",
                    "position": f"{item.get('position', '')}",
                    "inn": f"{item.get('inn'), ''}",
                }
                affilation.append(related)

    if json_dict["hasOrganizations"]:
        if len(json_dict["organizations"]):
            for item in json_dict["organizations"]:
                organization = {
                    "view": 'Участвует в деятельности коммерческих организаций"',
                    "name": f"{item.get('name', '')}",
                    "position": f"{item.get('workCombinationTime', '')}",
                    "inn": f"{item.get('inn'), ''}",
                }
                affilation.append(organization)
    return affilation
