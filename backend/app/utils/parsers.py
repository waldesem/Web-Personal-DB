import re

from sqlalchemy import select

from ..utils.folders import Folders
from ..models.classes import Statuses
from ..models.model import (
    Relation,
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


class Resume:

    def __init__(self, resume):
        for k, v in resume.items():
            if k in ["surname", "firstname", "patronymic"]:
                resume[k] = v.strip().upper()
        self.resume: dict = resume

    @staticmethod
    def get_person(surname, firstname, patronymic, birthday):
        return db.session.execute(
            select(Person).filter(
                Person.surname.ilike(surname),
                Person.firstname.ilike(firstname),
                Person.patronymic.ilike(patronymic),
                Person.birthday == birthday,
            )
        ).scalar_one_or_none()

    def change_status(self, status, user_id=None):
        self.resume["status_id"] = Status.get_id(status)
        self.resume["user_id"] = user_id
        db.session.commit()

    def check_resume(self):
        person = self.get_person(
            self.resume["surname"],
            self.resume["firstname"],
            self.resume.get("patronymic", ""),
            self.resume["birthday"],
        )
        if person:
            self.change_status(Statuses.repeat.value)
            return self.update_resume(person)
        else:
            self.change_status(Statuses.new.value)
            return self.add_resume()

    def update_resume(self, person):
        for k, v in self.resume.items():
            setattr(person, k, v)
        db.session.commit()
        return person.id

    def add_resume(self):
        person = Person(**self.resume)
        db.session.add(person)
        db.session.flush()
        person_id = person.id

        folders = Folders(
            person_id,
            self.resume["surname"],
            self.resume["firstname"],
            self.resume.get("patronymic", ""),
        )
        person.path = folders.create_main_folder()
        db.session.commit()
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
                    else self.resume.get("patronymic")
                ),
                self.resume["birthday"],
            )
            if relation:
                self.add_relation("Одно лицо", self.person_id, relation.id)


    def save_items(self):
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
            self.anketa["previous"],
            self.anketa["education"],
            self.anketa["staff"],
            self.anketa["document"],
            self.anketa["address"],
            self.anketa["contact"],
            self.anketa["workplace"],
            self.anketa["affilation"],
        ]
        for model, items in zip(models, items_lists):
            for item in items:
                if item:
                    item["person_id"] = self.person_id
                    db.session.add(model(**item))

        db.session.commit()

    @staticmethod
    def add_relation(relation, person_id, relation_id):
        db.session.add_all(
            [
                Relation(
                    relation=relation, person_id=person_id, relation_id=relation_id
                ),
                Relation(
                    relation=relation, person_id=relation_id, relation_id=person_id
                ),
            ]
        )
        db.session.commit()
        
    @staticmethod
    def parse_json(json_dict) -> None:
        json_data = {
            "resume": {
                "status_id": Status().get_id(Statuses.new.name),
                "region_id": Anketa.get_region_id(json_dict),
                "firstname": json_dict["firstName"].strip().upper(),
                "surname": json_dict["lastName"].strip().upper(),
                "birthday": json_dict["birthday"],
                "birthplace": json_dict["birthplace"].strip(),
                "country": json_dict["citizen"].strip(),
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
                case "ValidAddress":
                    json_data["address"].append(
                        {
                            "view": "Адрес проживания",
                            "address": json_dict["ValidAddress"],
                        }
                    )
                case "RegAddress":
                    json_data["address"].append(
                        {
                            "view": "Адрес регистрации",
                            "address": json_dict["RegAddress"],
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

    @staticmethod
    def get_region_id(json_dict):
        region_id = 1
        if "department" in json_dict:
            divisions = re.split(r"/", json_dict["department"].strip())
            for div in divisions:
                reg_id = Region().get_id(div)
                if reg_id:
                    region_id = reg_id
        return region_id
