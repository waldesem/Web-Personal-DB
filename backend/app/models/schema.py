from apiflask import Schema
from apiflask.fields import String, Date, Nested, Boolean, Integer
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from ..models.model import (
    Conclusion,
    Previous,
    Education,
    Relation,
    Status,
    User,
    Person,
    Affilation,
    Staff,
    Document,
    Address,
    Contact,
    Workplace,
    Check,
    Poligraf,
    Investigation,
    Inquiry,
    Message,
    Region,
    Role,
    Connect,
    Robot,
)


class RoleSchema(SQLAlchemyAutoSchema):
    """Create model for role"""

    class Meta:
        model = Role
        ordered = True


class UserSchema(SQLAlchemyAutoSchema):
    """Create model for user"""

    roles = Nested("RoleSchema", many=True)

    class Meta:
        model = User
        ordered = True
        include_fk = True
        exclude = (
            "password",
            "search_vector",
        )


class LoginSchema(Schema):
    """Create model for login"""

    username = String()
    password = String()
    new_pswd = String()


class MessageSchema(SQLAlchemyAutoSchema):
    """Create model for message"""

    class Meta:
        model = Message
        ordered = True


class PersonSchema(SQLAlchemyAutoSchema):
    """Create model for person"""

    class Meta:
        model = Person
        ordered = True
        include_fk = True
        exclude = ("search_vector",)


class RegionSchema(SQLAlchemyAutoSchema):
    """Create model for location"""

    class Meta:
        model = Region
        ordered = True


class StatusSchema(SQLAlchemyAutoSchema):
    """Create model for status"""

    class Meta:
        model = Status
        ordered = True


class RelationSchema(SQLAlchemyAutoSchema):
    """Create model for relation"""

    class Meta:
        model = Relation
        ordered = True


class DocumentSchema(SQLAlchemyAutoSchema):
    """Create model for document"""

    class Meta:
        model = Document
        ordered = True


class AddressSchema(SQLAlchemyAutoSchema):
    """Create model for address"""

    class Meta:
        model = Address
        ordered = True


class StaffSchema(SQLAlchemyAutoSchema):
    """Create model for staff"""

    class Meta:
        model = Staff
        ordered = True


class PreviousSchema(SQLAlchemyAutoSchema):
    """Create model for staff"""

    class Meta:
        model = Previous
        ordered = True


class EducationSchema(SQLAlchemyAutoSchema):
    """Create model for education"""

    class Meta:
        model = Education
        ordered = True


class WorkplaceSchema(SQLAlchemyAutoSchema):
    """Create model for workplace"""

    class Meta:
        model = Workplace
        ordered = True


class ContactSchema(SQLAlchemyAutoSchema):
    """Create model for contact"""

    class Meta:
        model = Contact
        ordered = True


class AffilationSchema(SQLAlchemyAutoSchema):
    """Create model for affilation"""

    class Meta:
        model = Affilation
        ordered = True


class CheckSchema(SQLAlchemyAutoSchema):
    """Create model for check"""

    class Meta:
        model = Check
        ordered = True
        include_fk = True
        dump_only = ("person_id",)


class RobotSchema(SQLAlchemyAutoSchema):
    """Create model for robot"""

    class Meta:
        model = Robot
        ordered = True
        dump_only = ("deadline",)

    path = String()


class ConclusionSchema(SQLAlchemyAutoSchema):
    """Create model for conclusion"""

    class Meta:
        model = Conclusion
        ordered = True


class InquirySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inquiry
        ordered = True
        include_fk = True
        dump_only = ("person_id",)


class InvestigationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Investigation
        ordered = True
        include_fk = True
        dump_only = ("person_id",)


class PoligrafSchema(SQLAlchemyAutoSchema):
    """Create model for poligraf"""

    class Meta:
        model = Poligraf
        ordered = True
        include_fk = True
        dump_only = ("person_id",)


class ConnectSchema(SQLAlchemyAutoSchema):
    """Create schema for Connections"""

    class Meta:
        model = Connect
        ordered = True
        exclude = ("search_vector",)


class InfoSchema(Schema):

    region_id = String()
    start = Date()
    end = Date()


"""Schemas for API endpoints"""

class NameWasChangedApi(Schema):
    """Nested schema for AnketaSchemaApi"""

    surname = String(required=False, attribute="firstNameBeforeChange")
    firstname = String(required=False, attribute="lastNameBeforeChange")
    patronymic = String(required=False, attribute="midNameBeforeChange")
    date_change = String(required=True, attribute="yearOfChange")
    reason = String(required=False)


class EducationApi(Schema):
    """Nested schema for AnketaSchemaApi"""

    view = String(required=True, attribute="educationType")
    name = String(required=False, attribute="institutionName")
    end = Integer(required=False, attribute="endYear")
    specialty = String(required=False, attribute="specialty")


class ExperienceApi(Schema):
    """Nested schema for AnketaSchemaApi"""

    start_date = String(required=True, attribute="beginDate")
    end_date = String(required=False, attribute="endDate")
    now_work = Boolean(required=True, attribute="currentJob")
    workplace = String(required=True, attribute="name")
    address = String(required=True)
    position = String(required=True)
    reason = String(required=False, attribute="fireReason")


class OrganizationsApi(Schema):
    """Nested schema for AnketaSchemaApi"""

    name = String(required=True)
    position = String(required=True)
    inn = String(required=True)


class RelatedPersonsOrganizationsApi(Schema):
    """Nested schema for AnketaSchemaApi"""

    name = String(required=True)
    position = String(required=True)
    inn = String(required=True)


class StateOrganizationsApi(Schema):
    """Nested schema for AnketaSchemaApi"""

    name = String(required=True)
    position = String(required=True)


class PublicOfficeOrganizationsApi(Schema):
    """Nested schema for AnketaSchemaApi"""

    name = String(required=True)
    position = String(required=True)


class AnketaSchemaApi(Schema):
    """Create schema for getting anketa"""

    positionName = String(required=True)
    department = String(required=False)
    lastName = String(required=True)
    firstName = String(required=True)
    midName = String(required=False)
    birthday = String(required=True)
    birthplace = String(required=True)
    citizen = String(required=True)
    additionalCitizenship = String(required=False)
    maritalStatus = String(required=False)
    regAddress = String(required=False)
    validAddress = String(required=True)
    contactPhone = String(required=True)
    email = String(required=False)
    inn = String(required=True)
    snils = String(required=True)
    passportSerial = String(required=True)
    passportNumber = String(required=True)
    passportIssueDate = String(required=True)
    passportIssuedBy = String(required=True)
    nameWasChanged = Nested(NameWasChangedApi, required=False, many=True)
    education = Nested(EducationApi, required=False, many=True)
    experience = Nested(ExperienceApi, required=False, many=True)
    organizations = Nested(OrganizationsApi, required=False, many=True)
    relatedPersonsOrganizations = Nested(
        RelatedPersonsOrganizationsApi, required=False, many=True
    )
    stateOrganizations = Nested(StateOrganizationsApi, required=False, many=True)
    publicOfficeOrganizations = Nested(
        PublicOfficeOrganizationsApi, required=False, many=True
    )