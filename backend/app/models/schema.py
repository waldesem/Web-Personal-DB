from apiflask import Schema
from apiflask.fields import String, Date, Nested
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema

from ..models.model import (
    Conclusion,
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


class RobotSchema(SQLAlchemyAutoSchema):
    """Create model for robot"""

    class Meta:
        model = Robot
        ordered = True


class ConclusionSchema(SQLAlchemyAutoSchema):
    """Create model for conclusion"""

    class Meta:
        model = Conclusion
        ordered = True


class InquirySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Inquiry
        ordered = True


class InvestigationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Investigation
        ordered = True


class PoligrafSchema(SQLAlchemyAutoSchema):
    """Create model for poligraf"""

    class Meta:
        model = Poligraf
        ordered = True


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


class AnketaSchemaApi(SQLAlchemySchema):
    """Create schema for sending anketa"""

    id = String()
    surname = String()
    firstname = String()
    patronymic = String()
    birthday = String()
    birthplace = String()
    snils = String()
    inn = String()
    series = String()
    number = String()
    agency = String()
    issue = String()
    address = String()