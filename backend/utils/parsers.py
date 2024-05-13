import re

from sqlalchemy import select
from sqlmodel import Session

from ..utils.folders import Folders
from ..models.classes import Statuses
from ..models.schema import AnketaSchemaApi
from ..models.model import (
    engine,
    Relation,
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
        for k, v in resume.__dict__.items():
            if k in ["surname", "firstname", "patronymic"]:
                resume[k] = v.strip().upper()
        self.resume: Person = resume

    @staticmethod
    def get_person(surname, firstname, patronymic, birthday):
        with Session(engine) as session:
            result = select(Person).filter(
                Person.surname.ilike(surname),
                Person.firstname.ilike(firstname),
                Person.patronymic.ilike(patronymic),
                Person.birthday == birthday,
            )
            return session.scalar(result)

    def change_status(self, status, user_id=None):
        with Session(engine) as session:
            self.resume.status_id = Status.get_id(status)
            self.resume.user_id = user_id
            session.commit()

    def check_resume(self):
        person = self.get_person(
            self.resume.surname,
            self.resume.firstname,
            self.resume.patronymic if hasattr(self.resume, "patronymic") else "",
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
                self.resume.patronymic if hasattr(self.resume, "patronymic") else "",
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
                (item.surname if hasattr(item, "surname") else self.resume.surname),
                (
                    item.firstname
                    if hasattr(item, "firstname")
                    else self.resume.firstname
                ),
                (
                    item.patronymic
                    if hasattr(item, "patronymic")
                    else (
                        self.resume.patronymic
                        if hasattr(self.resume, "patronymic")
                        else ""
                    )
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
                        relation=relation, person_id=self.person_id, relation_id=relation_id
                    ),
                    Relation(
                        relation=relation, person_id=relation_id, relation_id=self.person_id
                    ),
                ]
            )
            session.commit()

    def parse_resume(self) -> Person:
        return Person(
            status_id=Status().get_id(Statuses.new.name),
            region_id=Anketa.get_region_id(),
            firstname=self.data.firstName.strip().upper(),
            surname=self.data.lastName.strip().upper(),
            patronymic=(
                self.data.midName.strip().upper()
                if hasattr(self.data, "midName")
                else ""
            ),
            birthday=self.data.birthday,
            birthplace=self.data.birthplace.strip(),
            country=self.data.citizen.strip(),
            ext_country=(
                self.data.additionalCitizenship
                if hasattr(self.data, "additionalCitizenship")
                else ""
            ),
            marital=(
                self.data.maritalStatus if hasattr(self.data, "maritalStatus") else ""
            ),
            inn=self.data.inn if hasattr(self.data, "inn") else "",
            snils=self.data.snils if hasattr(self.data, "snils") else "",
        )

    def parse_items(self) -> dict:
        return dict(
            staff=Staff(
                position=self.data.positionName,
                department=(
                    self.data.department if hasattr(self.data, "department") else ""
                ),
                person_id=self.person_id,
            ),
            previous=[
                Previous(
                    surname=item.lastNameBeforeChange,
                    firstname=item.firstNameBeforeChange,
                    patronymic=item.midNameBeforeChange,
                    date_change=item.yearOfChange,
                    reason=item.reason,
                    person_id=self.person_id,
                )
                for item in self.data.nameWasChanged
                if len(self.data.nameWasChanged)
                and hasattr(self.data, "nameWasChanged")
            ],
            education=[
                Education(
                    view=item.educationType,
                    name=item.institutionName,
                    end=item.endYear,
                    specialty=item.specialty,
                    person_id=self.person_id,
                )
                for item in self.data.education
                if len(self.data.education) and hasattr(self.data, "education")
            ],
            workplace=[
                Workplace(
                    now_work=item.currentJob,
                    start_date=item.beginDate,
                    end_date=item.endDate,
                    workplace=item.name,
                    address=item.address,
                    position=item.position,
                    reason=item.fireReason,
                    person_id=self.person_id,
                )
                for item in self.data.experience
                if len(self.data.experience) and hasattr(self.data, "experience")
            ],
            address=[
                Address(
                    view="Адрес проживания",
                    address=self.data.validAddress,
                    person_id=self.person_id,
                ),
                Address(
                    view="Адрес регистрации",
                    address=self.data.regAddress,
                    person_id=self.person_id,
                ),
            ],
            contact=[
                Contact(
                    view="Телефон",
                    contact=self.data.contactPhone,
                    person_id=self.person_id,
                ),
                Contact(
                    view="Электронная почта",
                    contact=self.data.email,
                    person_id=self.person_id,
                ),
            ],
            document=[
                Document(
                    view="Паспорт",
                    number=self.data.passportNumber,
                    series=self.data.passportSerial,
                    issue=self.data.passportIssueDate,
                    agency=self.data.passportIssuedBy,
                    person_id=self.person_id,
                )
            ],
            affilation=[
                [
                    Affilation(
                        name=item.name,
                        position=item.position,
                        inn=item.inn,
                        person_id=self.person_id,
                    )
                    for item in self.data.organizations
                    if len(self.data.organizations)
                    and hasattr(self.data, "organizations")
                ]
                + [
                    Affilation(
                        name=item.name,
                        position=item.position,
                        inn=item.inn,
                        person_id=self.person_id,
                    )
                    for item in self.data.relatedPersonsOrganizations
                    if len(self.data.relatedPersonsOrganizations)
                    and hasattr(self.data, "relatedPersonsOrganizations")
                ]
                + [
                    Affilation(
                        name=item.name, position=item.position, person_id=self.person_id
                    )
                    for item in self.data.stateOrganizations
                    if len(self.data.stateOrganizations)
                    and hasattr(self.data, "stateOrganizations")
                ]
                + [
                    Affilation(
                        name=item.name, position=item.position, person_id=self.person_id
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
            divisions = re.split(r"/", self.data.department.strip())
            with Session(engine) as session:
                regions = session.exec(select(Region)).all()
                for reg in regions:
                    if reg.region in divisions:
                        region_id = reg.id
                        break
        return region_id
