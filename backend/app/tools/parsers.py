from datetime import datetime
import re

from ..tools.depends import current_user
from ..tools.folders import Folders
from ..tools.queries import select_single, execute
from .classes import Regions, Statuses


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
        stmt = """
        SELECT * FROM person
        WHERE surname = ?
        AND firstname = ?
        AND patronymic = ?
        AND birthday = ?
        """
        return select_single(stmt, (surname, firstname, patronymic, birthday))


    def update_status(self):
        person = self.get_person(
            self.resume["surname"],
            self.resume["firstname"],
            self.resume.get("patronymic", ""),
            self.resume["birthday"],
        )

        if person:
            return self.update_resume(person.id)
        else:
            status = Statuses.manual.name
            user_id = current_user["id"]

            query = """
                INSERT INTO person ({}) VALUES ({})
                RETURNING id
            """
            columns = ", ".join(self.resume.keys())
            values = ", ".join(["%s"] * len(self.resume))
            args = tuple(self.resume.values()) + (status, user_id)
            person_id = execute(query.format(columns, values), args)

            folders = Folders(
                person_id,
                self.resume["surname"],
                self.resume["firstname"],
                self.resume.get("patronymic", ""),
            )
            path = folders.create_main_folder()

            query = "UPDATE person SET path = %s WHERE id = %s"
            args = (path, person_id)
            execute(query, args)

            return person_id

    def update_resume(self, person_id, manual=False):
        columns, values = [], []
        for key in self.resume.keys():
            columns.append(key)
            values.append(self.resume[key])
        sql = (
            f"UPDATE person SET {','.join(key + '=?' for key in columns)}"
            f", updated = ?, user_id = ? WHERE id = ?"
        )
        values += [datetime.now(), current_user["id"], person_id]
        if manual:
            execute(sql, values)
        else:
            values.append(Statuses.manual.name)
            execute(sql, values)
        return person_id


class Anketa(Resume):
    def __init__(self, json_data):
        self.anketa = self.parse_json(json_data)
        super().__init__(self.anketa["resume"])
        self.person_id = self.update_status()

    def parse_anketa(self):
        if len(self.anketa["previous"]):
            self.parse_relations()
        self.save_items()
        return self.person_id

    def parse_relations(self):
        values = []
        for item in self.anketa["previous"]:
            surname = item.get("surname", self.resume["surname"])
            firstname = item.get("firstname", self.resume["firstname"])
            patronymic = item.get("patronymic", self.resume.get("patronymic", ""))
            birthday = self.resume["birthday"]
            relation = self.get_person(surname, firstname, patronymic, birthday)
            if relation:
                values.append(("Одно лицо", self.person_id, relation.id))
        if values:
            execute(
                "INSERT INTO relations (relation, person_id, relation_id) VALUES (?, ?, ?)",
                values,
            )

    def save_items(self):
        for table in [key for key in self.anketa.items() if key != "resume"]:
            execute(
                f"INSERT INTO {table} ({','.join(self.anketa[table].keys())}, person_id) \
                    VALUES ({','.join(self.anketa[table].values())}, ?)",
                (self.person_id,),
            )

    @staticmethod
    def parse_json(json_dict) -> None:
        json_data = {
            "resume": {
                "region_id": Anketa.get_region_id(json_dict),
                "firstname": json_dict["firstName"],
                "surname": json_dict["lastName"],
                "birthday": datetime.strptime(json_dict["birthday"], "%Y-%m-%d").date(),
                "birthplace": json_dict["birthplace"],
                "country": json_dict["citizen"],
            },
            "previous": [],
            "educations": [],
            "workplaces": [],
            "addresses": [],
            "contacts": [],
            "documents": [],
            "affilations": [],
            "staffs": [
                {
                    "position": json_dict.get("positionName"),
                    "department": json_dict.get("department"),
                }
            ],
        }
        for item in json_dict:
            match item:
                case "midName":
                    json_data["resume"]["patronymic"] = json_dict["midName"]
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
                            "number": json_dict["passportNumber"],
                            "series": json_dict.get("passportSerial"),
                            "issue": datetime.strptime(
                                json_dict["passportIssueDate"], "%Y-%m-%d"
                            ).date()
                            if json_dict.get("passportIssueDate")
                            else None,
                            "agency": json_dict.get("passportIssuedBy"),
                        }
                    )
                case (
                    "publicOfficeOrganizations"
                    | "stateOrganizations"
                    | "relatedPersonsOrganizations"
                    | "organizations"
                ):
                    if len(json_dict[item]):
                        for i in json_dict[item]:
                            org = {}
                            match item:
                                case "publicOfficeOrganizations":
                                    org["view"] = (
                                        "Являлся государственным или муниципальным служащим"
                                    )
                                case "stateOrganizations":
                                    org["view"] = (
                                        "Являлся государственным должностным лицом"
                                    )
                                case "relatedPersonsOrganizations":
                                    org["view"] = (
                                        "Связанные лица работают в госудраственных организациях"
                                    )
                                case "organizations":
                                    org["view"] = (
                                        "Участвует в деятельности коммерческих организаций"
                                    )
                            for k, v in i.items():
                                match k:
                                    case "name":
                                        org["name"] = v
                                    case "position":
                                        org["position"] = v
                                    case "inn":
                                        org["inn"] = v
                            json_data["affilations"].append(org)

                case "previous":
                    if len(json_dict["previous"]):
                        for item in json_dict["previous"]:
                            previous = {}
                            for k, v in item.items():
                                match k:
                                    case "firstNameBeforeChange":
                                        previous["firstname"] = k
                                    case "lastNameBeforeChange":
                                        previous["surname"] = k
                                    case "midNameBeforeChange":
                                        previous["patronymic"] = k
                                    case "yearOfChange":
                                        previous["date_change"] = k
                                    case "reason":
                                        previous["reason"] = v
                            json_data["previous"].append(previous)
                case "education":
                    if len(json_dict["education"]):
                        for item in json_dict["education"]:
                            education = {}
                            for k, v in item.items():
                                match k:
                                    case "educationType":
                                        education["view"] = v
                                    case "institutionName":
                                        education["name"] = v
                                    case "endYear":
                                        education["finish"] = v
                                    case "specialty":
                                        education["specialty"] = v
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
        region = Regions.main.name
        if "department" in json_dict and json_dict.get("department"):
            for reg in [r for r in Regions]:
                if reg.value.upper() in re.split(r"/", json_dict["department"].upper()):
                    region = reg.name
                    break
        return region
