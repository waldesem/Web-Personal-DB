from datetime import datetime
import re

from ..tools.folders import Folders
from ..tools.queries import select_all, select_single, execute
from .classes import Statuses


class Resume:

    def __init__(self, resume):
        for k, v in resume.items():
            if k in ["surname", "firstname", "patronymic"]:
                resume[k] = v.strip().upper()
            elif k == "birthday":
                resume[k] = datetime.strptime(v, "%Y-%m-%d").date()
        self.resume: dict = resume

    @staticmethod
    def get_person(surname, firstname, patronymic, birthday):
        return select_single(
            "SELECT * FROM person WHERE surname = ? AND firstname = ? AND patronymic = ? AND birthday = ?",
            (surname, firstname, patronymic, birthday,),
        )

    def change_status(self, status, user_id=None):
        status = select_single(
            "SELECT * FROM statuses WHERE name = ?", 
            (status,)
        )
        execute(
            "UPDATE person SET status_id = ? WHERE user_id = ?", (status["id"], user_id)
        )

    def check_resume(self):
        person = self.get_person(
            self.resume["surname"],
            self.resume["firstname"],
            self.resume.get("patronymic", ""),
            self.resume["birthday"],
        )
        if person:
            self.change_status(Statuses.repeat.value)
            return self.update_resume(person.id)
        else:
            self.change_status(Statuses.new.value)
            return self.add_resume()

    def update_resume(self, person_id):
        execute(
            f"UPDATE person SET {self.resume}, updated = ? WHERE id = ?",
            datetime.now(), person_id
        )
        return person_id

    def add_resume(self):
        person_id = execute(
            "INSERT INTO person ({}, created) VALUES ({})".format(
                ", ".join(self.resume.keys()),
                ", ".join(self.resume.values()),
            ), datetime.now(),
        )

        folders = Folders(
            person_id,
            self.resume["surname"],
            self.resume["firstname"],
            self.resume.get("patronymic", ""),
        )
        path = folders.create_main_folder()
        execute(
            "UPDATE person SET path = ? WHERE id = ?", (path, person_id)
        )
        return person_id


class Anketa(Resume):

    def __init__(self, json_data):
        self.anketa = self.parse_json(json_data)
        super().__init__(self.anketa["resume"])
        self.person_id = self.check_resume()

    def parse_anketa(self):
        if len(self.anketa["previous"]):
            self.parse_relations()
        self.save_items()
        return self.person_id


    def parse_relations(self):
        for item in self.anketa["previous"]:
            relation = self.get_person(
                (
                    item.get("surname")
                    if item.get("surname")
                    else self.resume["surname"]
                ),
                (
                    item.get("firstname")
                    if item.get("firstname")
                    else self.resume["firstname"]
                ),
                (
                    item.get("patronymic")
                    if item.get("patronymic")
                    else self.resume.get("patronymic", "")
                ),
                self.resume["birthday"],
            )
            if relation:
                execute(
                    "INSERT INTO relations (relation, person_id, relation_id) VALUES(?, ?, ?)", 
                    ("Одно лицо", self.person_id, relation.id)    
                )

    def save_items(self):
        tables = [
            "previous", 
            "educations", 
            "staffs", 
            "documents", 
            "addresses", 
            "contacts", 
            "workplaces", 
            "affilations"
        ]
        items_lists = [
            self.anketa["previou"],
            self.anketa["education"],
            self.anketa["staff"],
            self.anketa["document"],
            self.anketa["addresse"],
            self.anketa["contact"],
            self.anketa["workplace"],
            self.anketa["affilation"],
        ]
        for table, item in zip(tables, items_lists):
            execute(
                f"INSERT INTO {table} ({','.join(item.keys())}, person_id) VALUES ({','.join(item.values())}, ?)", 
                self.person_id 
            )
        
    @staticmethod
    def parse_json(json_dict) -> None:
        status = select_single(
            "SELECT * FROM statuses WHERE name = ?", (Statuses.new.name,)
        )
        json_data = {
            "resume": {
                "status_id": status["id"],
                "region_id": Anketa.get_region_id(json_dict),
                "firstname": json_dict["firstName"].strip().upper(),
                "surname": json_dict["lastName"].strip().upper(),
                "birthday": json_dict["birthday"],
                "birthplace": json_dict["birthplace"],
                "country": json_dict["citizen"],
            },
            "previous": [],
            "education": [],
            "workplace": [],
            "address": [],
            "contact": [],
            "document": [],
            "affilation": [],
            "staff": [
                {
                    "position": json_dict.get("positionName"),
                    "department": json_dict.get("department"),
                }
            ],
        }
        for item in json_dict:
            match item:
                case "midName":
                    json_data["resume"]["patronymic"] = (
                        json_dict["midName"].strip().upper()
                    )
                case "additionalCitizenship":
                    json_data["resume"]["ext_country"] = json_dict[
                        "additionalCitizenship"
                    ]
                case "maritalStatus":
                    json_data["resume"]["marital"] = json_dict["maritalStatus"]
                case "inn":
                    json_data["resume"]["inn"] = json_dict["inn"].strip()
                case "snils":
                    json_data["resume"]["snils"] = json_dict["snils"].strip()
                case "validAddress":
                    json_data["address"].append(
                        {
                            "view": "Адрес проживания",
                            "address": json_dict["validAddress"],
                        }
                    )
                case "regAddress":
                    json_data["address"].append(
                        {
                            "view": "Адрес регистрации",
                            "address": json_dict["regAddress"],
                        }
                    )
                case "contactPhone":
                    json_data["contact"].append(
                        {"view": "Телефон", "contact": json_dict["contactPhone"]}
                    )
                case "email":
                    json_data["contact"].append(
                        {"view": "Электронная почта", "contact": json_dict["email"]}
                    )
                case "passportNumber":
                    json_data["document"].append(
                        {
                            "view": "Паспорт",
                            "number": json_dict["passportNumber"].strip(),
                            "series": json_dict.get("passportSerial").strip(),
                            "issue": datetime.strptime(json_dict.get("passportIssueDate"), "%Y-%m-%d").date(),
                            "agency": json_dict.get("passportIssuedBy"),
                        }
                    )
                case "publicOfficeOrganizations":
                    if len(json_dict["publicOfficeOrganizations"]):
                        for item in json_dict["publicOfficeOrganizations"]:
                            public = {
                                "view": "Являлся государственным или муниципальным служащим",
                                "name": f"{item.get('name', '')}",
                                "position": f"{item.get('position', '')}",
                            }
                            json_data["affilations"].append(public)

                case "stateOrganizations":
                    if len(json_dict["stateOrganizations"]):
                        for item in json_dict["stateOrganizations"]:
                            state = {
                                "view": "Являлся государственным должностным лицом",
                                "name": f"{item.get('name', '')}",
                                "position": f"{item.get('position', '')}",
                            }
                            json_data["affilations"].append(state)

                case "relatedPersonsOrganizations":
                    if len(json_dict["relatedPersonsOrganizations"]):
                        for item in json_dict["relatedPersonsOrganizations"]:
                            related = {
                                "view": "Связанные лица работают в госудраственных организациях",
                                "name": f"{item.get('name', '')}",
                                "position": f"{item.get('position', '')}",
                                "inn": f"{item.get('inn'), ''}",
                            }
                            json_data["affilations"].append(related)

                case "organizations":
                    if len(json_dict["organizations"]):
                        for item in json_dict["organizations"]:
                            organization = {
                                "view": 'Участвует в деятельности коммерческих организаций"',
                                "name": f"{item.get('name', '')}",
                                "position": f"{item.get('workCombinationTime', '')}",
                                "inn": f"{item.get('inn'), ''}",
                            }
                            json_data["affilations"].append(organization)
                case "previous":
                    if len(json_dict["previous"]):
                        for item in json_dict["previous"]:
                            previous = dict(
                                firstname = item.get(
                                    "firstNameBeforeChange", ""
                                ),
                                surname = item.get("lastNameBeforeChange", ""),
                                patronymic = item.get("midNameBeforeChange", ""),
                                date_change = str(item.get("yearOfChange", "")),
                                reason = str(item.get("reason", ""))
                            )
                            json_data["previous"].append(previous)
                case "education":
                    if len(json_dict["education"]):
                        for item in json_dict["education"]:
                            education = dict(
                                view = item.get("educationType", ""),
                                name = item.get("institutionName", ""),
                                end = item.get("endYear", "н.в."),
                                specialty = item.get("specialty", ""),
                            )
                            json_data["education"].append(education)
                case "experience":
                    if len(json_dict["experience"]):
                        for exp in json_dict["experience"]:
                            work = {}
                            for key, value in exp.items():
                                match key:
                                    case "beginDate":
                                        work["start_date"] = datetime.strptime(
                                            value, "%Y-%m-%d"
                                        ).date()
                                    case "endDate":
                                        work["end_date"] = datetime.strptime(
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
                        json_data["workplace"].append(work)
        return json_data

    @staticmethod
    def get_region_id(json_dict):
        region_id = 1
        if "department" in json_dict:
            divisions = re.split(r"/", json_dict["department"].strip())
            result = select_all("SELECT * FROM regions")
            for div in divisions:
                for item in result:
                    if item['region'] == div:
                        region_id = item['id']
                        break
        return region_id
