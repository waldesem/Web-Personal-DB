import re

from sqlalchemy import select
from sqlmodel import Session

from ..models.classes import Statuses
from ..models.model import (
    Address,
    Affilation,
    Contact,
    Document,
    Education,
    Person,
    Previous,
    Region,
    Relation,
    Staff,
    Status,
    Workplace,
    engine,
)
from ..models.schema import AnketaSchemaApi
from ..utils.folders import Folders


class Resume:
    def __init__(self, resume: Person):
        self.resume: Person = resume
        self.resume.surname = resume.surname.strip().upper()
        self.resume.firstname = resume.firstname.strip().upper()
        self.resume.patronymic = (
            getattr(resume, "patronymic").strip().upper()
            if self.resume.patronymic
            else ""
        )
        self.resume.birthday = resume.birthday

    @staticmethod
    def get_person(surname, firstname, patronymic, birthday):
        with Session(engine) as session:
            return session.exec(
                select(Person).filter(
                    Person.surname.ilike(surname),
                    Person.firstname.ilike(firstname),
                    Person.patronymic.ilike(patronymic if patronymic else "%"),
                    Person.birthday == birthday,
                )
            ).one_or_none()

    def change_status(self, status, user_id=None):
        with Session(engine) as session:
            self.resume.status_id = Status.get_id(status)
            self.resume.user_id = user_id
            session.commit()

    def check_resume(self):
        person = self.get_person(
            self.resume.surname,
            self.resume.firstname,
            self.resume.patronymic,
            self.resume.birthday,
        )
        if person:
            self.change_status(Statuses.repeat.value)
            return self.update_resume(person)
        else:
            self.change_status(Statuses.new.value)
            return self.add_resume()

    def update_resume(self, person):
        with Session(engine) as session:
            for k, v in self.resume.__dict__.items():
                setattr(person, k, v)
            session.commit()
            return person.id

    def add_resume(self):
        with Session(engine) as session:
            session.add(self.resume)
            session.flush()
            person_id = self.resume.id

            folders = Folders(
                person_id,
                self.resume.surname,
                self.resume.firstname,
                self.resume.patronymic,
            )
            self.resume.path = folders.create_main_folder()
            session.commit()
            return person_id


class Anketa(Resume):
    def __init__(self, data):
        self.data: AnketaSchemaApi = data
        self.resume: Person = self.parse_resume()
        super().__init__(self.resume)
        self.person_id = self.check_resume()
        self.items = self.parse_items()

    def parse_anketa(self):
        if self.items.get("previous") and len(self.items.get("previous")):
            self.parse_relations()
        self.save_items()
        return self.person_id

    def parse_relations(self):
        for item in self.items["previous"]:
            relation = self.get_person(
                getattr(item, "surname", self.resume.surname),
                getattr(item, "firstname", self.resume.firstname),
                getattr(
                    item,
                    "patronymic",
                    self.resume.patronymic if self.resume.patronymic else "",
                ),
                self.resume["birthday"],
            )
            if relation:
                self.add_relation("Одно лицо", relation.id)

    def save_items(self):
        with Session(engine) as session:
            for _, item in self.items.items():
                session.add_all(item)
                session.commit()

    def add_relation(self, relation, relation_id):
        with Session(engine) as session:
            session.add_all(
                [
                    Relation(
                        relation=relation,
                        person_id=self.person_id,
                        relation_id=relation_id,
                    ),
                    Relation(
                        relation=relation,
                        person_id=relation_id,
                        relation_id=self.person_id,
                    ),
                ]
            )
            session.commit()

    def parse_resume(self) -> Person:
        return Person(
            status_id=Status().get_id(Statuses.new.name),
            region_id=Anketa.get_region_id(),
            firstname=self.data.firstName,
            surname=self.data.lastName,
            patronymic=getattr(self.data, "midName", ""),
            birthday=self.data.birthday,
            birthplace=getattr(self.data, "birthplace", ""),
            country=getattr(self.data, "citizen", ""),
            ext_country=getattr(self.data, "additionalCitizenship", ""),
            marital=getattr(self.data, "maritalStatus", ""),
            inn=getattr(self.data, "inn", ""),
            snils=getattr(self.data, "snils", ""),
        )

    def parse_items(self) -> dict:
        return dict(
            staff=[
                Staff(
                    position=self.data.positionName,
                    department=getattr(self.data, "department", ""),
                    person_id=self.person_id,
                )
            ],
            previous=[
                Previous(
                    surname=getattr(item, "lastNameBeforeChange", ""),
                    firstname=getattr(item, "firstNameBeforeChange", ""),
                    patronymic=getattr(item, "midNameBeforeChange", ""),
                    date_change=getattr(item, "yearOfChange", ""),
                    reason=getattr(item, "reason", ""),
                    person_id=self.person_id,
                )
                for item in self.data.nameWasChanged
                if len(self.data.nameWasChanged)
                and hasattr(self.data, "nameWasChanged")
            ],
            education=[
                Education(
                    view=getattr(item, "educationType", ""),
                    name=getattr(item, "institutionName", ""),
                    end=getattr(item, "endYear", ""),
                    specialty=getattr(item, "specialty", ""),
                    person_id=self.person_id,
                )
                for item in self.data.education
                if len(self.data.education) and hasattr(self.data, "education")
            ],
            workplace=[
                Workplace(
                    now_work=getattr(item, "currentJob", False),
                    start_date=getattr(item, "beginDate", ""),
                    end_date=getattr(item, "endDate", ""),
                    workplace=getattr(item, "name", ""),
                    address=getattr(item, "address", ""),
                    position=getattr(item, "position", ""),
                    reason=getattr(item, "fireReason", ""),
                    person_id=self.person_id,
                )
                for item in self.data.experience
                if len(self.data.experience) and hasattr(self.data, "experience")
            ],
            address=[
                Address(
                    view="Адрес проживания",
                    address=getattr(self.data, "validAddress", ""),
                    person_id=self.person_id,
                ),
                Address(
                    view="Адрес регистрации",
                    address=getattr(self.data, "regAddress", ""),
                    person_id=self.person_id,
                ),
            ],
            contact=[
                Contact(
                    view="Телефон",
                    contact=getattr(self.data, "contactPhone", ""),
                    person_id=self.person_id,
                ),
                Contact(
                    view="Электронная почта",
                    contact=getattr(self.data, "contactEmail", ""),
                    person_id=self.person_id,
                ),
            ],
            document=[
                Document(
                    view="Паспорт",
                    number=getattr(self.data, "passportNumber", ""),
                    series=getattr(self.data, "passportSerial", ""),
                    issue=getattr(self.data, "passportIssueDate", ""),
                    agency=getattr(self.data, "passportIssuedBy", ""),
                    person_id=self.person_id,
                )
            ],
            affilation=[
                [
                    Affilation(
                        name=getattr(item, "name", ""),
                        position=getattr(item, "position", ""),
                        inn=getattr(item, "inn", ""),
                        person_id=self.person_id,
                    )
                    for item in self.data.organizations
                    if len(self.data.organizations)
                    and hasattr(self.data, "organizations")
                ]
                + [
                    Affilation(
                        name=getattr(item, "name", ""),
                        position=getattr(item, "position", ""),
                        inn=getattr(item, "inn", ""),
                        person_id=self.person_id,
                    )
                    for item in self.data.relatedPersonsOrganizations
                    if len(self.data.relatedPersonsOrganizations)
                    and hasattr(self.data, "relatedPersonsOrganizations")
                ]
                + [
                    Affilation(
                        name=getattr(item, "name", ""),
                        position=getattr(item, "position", ""),
                        person_id=self.person_id,
                    )
                    for item in self.data.stateOrganizations
                    if len(self.data.stateOrganizations)
                    and hasattr(self.data, "stateOrganizations")
                ]
                + [
                    Affilation(
                        name=getattr(item, "name", ""),
                        position=getattr(item, "position", ""),
                        person_id=self.person_id,
                    )
                    for item in self.data.publicOfficeOrganizations
                    if len(self.data.publicOfficeOrganizations)
                    and hasattr(self.data, "publicOfficeOrganizations")
                ]
            ],
        )

    def get_region_id(self):
        region_id = 1
        if hasattr(self.data, "department"):
            divisions = re.split(r"/", self.data.department)
            with Session(engine) as session:
                regions = session.exec(select(Region)).all()
                for reg in regions:
                    if reg.region in divisions:
                        region_id = reg.id
                        break
        return region_id
