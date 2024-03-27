import re
import json
from datetime import datetime

from ..models.model import Region, Status
from ..models.classes import Statuses


def parse_json(file) -> None:
    with open(file, "r", newline="", encoding="utf-8-sig") as f:

        json_dict = json.load(f)
        json_dict = json.load(f)
        json_data = dict(
            resume = {},
            addresses = [],
            contacts = [],
            workplaces = [],
            documents = [],
            staffs = [],
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
                    json_data["resume"]["firstName"] = value.strip().upper()
                case "midName":
                    json_data["resume"]["patronymic"] = value.strip().upper()
                case "nameWasChanged":
                    previous = ""
                    if len(value):
                        for item in value:
                            firstNameBeforeChange = item.get(
                                "firstNameBeforeChange", ""
                            )
                            lastNameBeforeChange = item.get("lastNameBeforeChange", "")
                            midNameBeforeChange = item.get("midNameBeforeChange", "")
                            yearOfChange = str(item.get("yearOfChange", ""))
                            reason = str(item.get("reason", ""))
                            previous = previous + (
                                f"{yearOfChange} - {firstNameBeforeChange} "
                                f"{lastNameBeforeChange} {midNameBeforeChange}, "
                                f"{reason}; "
                            )
                        json_data["resume"]["previous"] = previous.rstrip("; ")
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
                    education = ""
                    if len(json_dict["education"]):
                        for item in json_dict["education"]:
                            institutionName = item.get("institutionName", "")
                            endYear = item.get("endYear", "н.в.")
                            specialty = item.get("specialty", "")
                            education = (
                                education
                                + f"{str(endYear)} - {institutionName}, {specialty}; "
                            )
                        json_data["resume"]["education"] = education.rstrip("; ")
                case "passportNumber":
                    json_data["documents"].append(
                        {
                            "view": "Паспорт",
                            "number": value,
                            "series": json_dict.get("passportSerial", ""),
                            "issue": json_dict.get("passportIssueDate", ""),
                            "agency": json_dict.get("passportIssuedBy", ""),
                        }
                    )
                case "regAddress":
                    json_data["addresses"].append(
                        {"view": "Адрес регистрации", "address": value}
                    )
                case "validAddress":
                    json_data["addresses"].append(
                        {"view": "Адрес проживания", "address": value}
                    )
                case "contactPhone":
                    json_data["contacts"].append({"view": "Телефон", "contact": value})
                case "email":
                    json_data["contacts"].append({"view": "E-mail", "contact": value})
                case "positionName":
                    json_data["staffs"].append(
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
                                    case "name":
                                        work["workplace"] = value
                                    case "address":
                                        work["address"] = value
                                    case "position":
                                        work["position"] = value
                                    case "fireReason":
                                        work["reason"] = value
                        json_data["workplaces"].append(work)
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
