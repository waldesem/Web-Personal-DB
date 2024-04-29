import re

import httpx
from sqlalchemy import select

from ..utils.folders import Folders
from ..models.classes import Statuses
from ..models.schema import ResumeSchemaApi
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


class Personal:

    def __init__(self, person_id):
        self.anketa = db.session.get(Person, person_id)

    def change_status(self, status, user_id=None):
        self.anketa.status_id = Status.get_id(status)
        self.anketa.user_id = user_id
        db.session.commit()

    def send_anketa(self):
        if self.anketa.status_id in (
            Status.get_id(Statuses.new.value),
            Status.get_id(Statuses.update.value),
            Status.get_id(Statuses.repeat.value),
            Status.get_id(Statuses.manual.value),
            Status.get_id(Statuses.robot.value),
        ):
            docum = db.session.execute(
                select(Document)
                .filter_by(person_id=self.anketa.id)
                .order_by(Document.id.desc())
            ).scalar_one_or_none()
            addr = db.session.execute(
                select(Address)
                .filter(
                    Address.person_id == self.anketa.id,
                    Address.view.ilike("%регистрац%"),
                )
                .order_by(Address.id.desc())
            ).scalar_one_or_none()
            if not docum or not addr:
                return "error"
            serial = ResumeSchemaApi().dump(
                {
                    "id": self.anketa.id,
                    "surname": self.anketa.surname,
                    "firstname": self.anketa.firstname,
                    "patronymic": self.anketa.patronymic,
                    "birthday": self.anketa.birthday,
                    "birthplace": self.anketa.birthplace,
                    "snils": self.anketa.snils,
                    "inn": self.anketa.inn,
                    "series": docum.series,
                    "number": docum.number,
                    "agency": docum.agency,
                    "issue": docum.issue,
                    "address": addr.address,
                }
            )
            try:
                response = httpx.post(
                    url="http://127.0.0.1:5001", json=serial, timeout=5
                )
                response.raise_for_status()
                return "send"
            except httpx.HTTPError as e:
                return "error"
        else:
            return "error"


class Resume:

    def __init__(self, resume):
        for k, v in resume.items():
            if k in ["surname", "firstname", "patronymic"]:
                resume[k] = v.strip().upper()
        self.resume = resume

    @staticmethod
    def get_person(surname, firstname, patronymic, birthday):
        return db.session.execute(
            select(Person).filter(
                Person.surname.ilike(surname),
                Person.firstname.ilike(firstname),
                Person.patronymic.ilike(patronymic),
                Person.birthday == birthday,
            )
        ).one_or_none()

    def check_resume(self):
        person = self.get_person(
            self.resume["surname"],
            self.resume["firstname"],
            self.resume.get("patronymic", ""),
            self.resume["birthday"],
        )
        return self.update_resume(person) if person else self.add_resume()

    def update_resume(self, person):
        for k, v in self.resume.items():
            setattr(person, k, v)
        db.session.commit()
        return person.id

    def add_resume(self):
        self.resume["status_id"] = Status().get_id(Statuses.new.value)
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
        self.parse_relations()
        self.save_items()
        return self.person_id

    def parse_relations(self):
        if len(self.anketa["previous"]):
            for item in self.anketa["previous"]:
                prev = self.get_person(
                    item.get("surname")
                    if item.get("surname")
                    else self.resume["surname"],

                    item.get("firstname")
                    if item.get("firstname")
                    else self.resume["firstname"],

                    item.get("patronymic")
                    if item.get("patronymic")
                    else self.resume.get("patronymic"),
                    
                    self.resume["birthday"],
                )
                if prev:
                    db.session.add_all(
                        [
                            Relation(
                                relation="Одно лицо",
                                person_id=self.person_id,
                                relation_id=prev.id,
                            ),
                            Relation(
                                relation="Одно лицо",
                                person_id=prev.id,
                                relation_id=self.person_id,
                            ),
                        ]
                    )
        db.session.commit()

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
                    db.session.add(model(**item | {"person_id": self.person_id}))

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

    @staticmethod
    def get_region_id(json_dict):
        region_id = 1
        if "department" in json_dict:
            divisions = re.split(r"/", json_dict["department"].strip())
            for div in divisions:
                region = Region().get_id(div)
                if region:
                    region_id = region
        return region_id
