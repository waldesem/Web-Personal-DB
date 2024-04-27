from apiflask import Schema
from apiflask.fields import String, Date, Nested, DateTime, Boolean, Integer
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema

from ..models.model import (
    Conclusion,
    Previous,
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


class SearchSchema(Schema):
    search = String(default="")


class SortSchema(SearchSchema):
    sort = String(default="id")
    order = String(default="desc")


class ActionSchema(Schema):
    action = String()


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


class RefreshSchema(Schema):
    """Create model for refresh"""

    access_token = String()


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


class InfoSchema(SQLAlchemySchema):

    region_id = String()
    start = Date()
    end = Date()


class GptInputSchema(SQLAlchemySchema):

    query = String()


class GptOutputSchema(SQLAlchemySchema):

    answer = String()


"""Schemas for API endpoints"""


class ResumeSchemaApi(SQLAlchemySchema):
    """Create schema for sending anketa"""

    id = String()
    surname = String()
    firstname = String()
    patronymic = String()
    birthday = Date()
    birthplace = String()
    snils = String()
    inn = String()
    series = String()
    number = String()
    agency = String()
    issue = Date()
    address = String()


class NameWasChanged(SQLAlchemySchema):
    """Nested schema for AnketaSchemaApi"""

    firstNameBeforeChange = String(required=False)
    lastNameBeforeChange = String(required=False)
    midNameBeforeChange = String(required=False)
    yearOfChange = String(required=False)
    reason = String(required=False)


class Education(SQLAlchemySchema):
    """Nested schema for AnketaSchemaApi"""

    educationType = String(required=False)
    institutionName = String(required=False)
    beginYear = Integer(required=False)
    endYear = Integer(required=False)
    specialty = String(required=False)


class Experience(SQLAlchemySchema):
    """Nested schema for AnketaSchemaApi"""

    beginDate = String(required=False)
    endDate = String(required=False)
    currentJob = Boolean(required=False)
    name = String(required=False)
    address = String(required=False)
    phone = String(required=False)
    activityType = String(required=False)
    position = String(required=False)
    possibilityContactEmployer = Boolean(required=False)
    fireReason = String(required=False)


class Organizations(SQLAlchemySchema):
    """Nested schema for AnketaSchemaApi"""

    name = String(required=False)
    position = String(required=False)
    inn = String(required=False)


class RelatedPersonsOrganizations(SQLAlchemySchema):
    """Nested schema for AnketaSchemaApi"""

    name = String(required=False)
    position = String(required=False)
    inn = String(required=False)


class StateOrganizations(SQLAlchemySchema):
    """Nested schema for AnketaSchemaApi"""

    name = String(required=False)
    position = String(required=False)


class PublicOfficeOrganizations(SQLAlchemySchema):
    """Nested schema for AnketaSchemaApi"""
    
    name = String(required=False)
    position = String(required=False)


class AnketaSchemaApi(SQLAlchemySchema):
    """Create schema for getting anketa"""

    positionName = String(required=True)
    department = String(required=False)
    statusDate = String(required=False)
    lastName = String(required=True)
    firstName = String(required=True)
    midName = String(required=False)
    hasNameChanged = Boolean(required=True)
    birthday = String(required=True)
    birthplace = String(required=True)
    citizen = String(required=True)
    hasAdditionalCitizenship = Boolean(required=True)
    maritalStatus = String(required=True)
    regAddress = String(required=False)
    validAddress = String(required=True)
    contactPhone = String(required=True)
    email = String(required=False)
    hasInn = Boolean(required=True)
    inn = String(required=False)
    hasSnils = Boolean(required=True)
    snils = String(required=False)
    passportSerial = String(required=True)
    passportNumber = String(required=True)
    passportIssueDate = String(required=True)
    passportIssuedBy = String(required=True)
    hasJob = Boolean(required=True)
    hasPublicOfficeOrganizations = Boolean(required=True)
    hasStateOrganizations = Boolean(required=True)
    hasRelatedPersonsOrganizations = Boolean(required=True)
    hasMtsRelatedPersonsOrganizations = Boolean(required=True)
    hasOrganizations = Boolean(required=True)
    nameWasChanged = Nested(NameWasChanged, required=False, many=True)
    education = Nested(Education, required=False, many=True)
    experience = Nested(Experience, required=False, many=True)
    organizations = Nested(Organizations, required=False, many=True)
    relatedPersonsOrganizations = Nested(
        RelatedPersonsOrganizations, required=False, many=True
    )
    stateOrganizations = Nested(StateOrganizations, required=False, many=True)
    publicOfficeOrganizations = Nested(
        PublicOfficeOrganizations, required=False, many=True
    )
