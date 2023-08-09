from apiflask import Schema
from flask_marshmallow import Marshmallow
from marshmallow import fields

from ..models.model import Relation, User, Person, Staff, Document, Address, Contact, Workplace, \
    Check, Registry, Poligraf, Investigation, Inquiry, Report, Log, Region

ma = Marshmallow()

class LogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Log
        ordered = True
        

class UserSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for user"""
    region_id = ma.auto_field()

    class Meta:
        model = User
        ordered = True


class LocationSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for location"""
    class Meta:
        model = Region 
        ordered = True


class LoginSchema(Schema):
    """ Create model for login"""

    username = fields.String()
    password = fields.String()
    new_pswd = fields.String()
    conf_pswd = fields.String()
 

class MessageSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for message"""
    class Meta:
        model = Report
        ordered = True


class MessagesSchema(ma.SQLAlchemySchema):
    """ Create model for messages list"""
    
    messages = fields.Nested(MessageSchema, many=True)


class PersonSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for person"""
    region_id = ma.auto_field()

    class Meta:
        model = Person
        ordered = True


class RelationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Relation
        ordered = True


class DocumentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Document
        ordered = True


class AddressSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Address
        ordered = True


class StaffSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Staff
        ordered = True


class WorkplaceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workplace
        ordered = True


class ContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Contact
        ordered = True


class CheckSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Check
        ordered = True
        

class InvestigationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Investigation
        ordered = True


class InquirySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inquiry
        ordered = True


class PoligrafSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Poligraf
        ordered = True


class RegistrySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Registry
        ordered = True


class AnketaSchema(ma.SQLAlchemySchema):
    """ Create model for sending anketa on check to API"""

    resume = PersonSchema()
    document = DocumentSchema()
    address = AddressSchema()


class ResumeSchema(ma.SQLAlchemySchema):
    """ Create model to get resume from API"""

    resume = fields.Nested(PersonSchema())
    document = fields.Nested(DocumentSchema())
    staff = fields.Nested(StaffSchema())
    addresses = fields.List(fields.Nested(AddressSchema()))
    workplaces = fields.List(fields.Nested(WorkplaceSchema()))
    contacts = fields.List(fields.Nested(ContactSchema()))


class ProfileSchema(ma.SQLAlchemySchema):
    """ Create model for rendering profile on page"""

    resume = fields.Nested(PersonSchema)
    documents = fields.Nested(DocumentSchema, many=True)
    addresses = fields.Nested(AddressSchema, many=True)
    contacts = fields.Nested(ContactSchema, many=True)
    workplaces = fields.Nested(WorkplaceSchema, many=True)
    staffs = fields.Nested(StaffSchema, many=True)
    relations = fields.Nested(RelationSchema, many=True)
    checks = fields.Nested(CheckSchema, many=True)
    registries = fields.Nested(RegistrySchema, many=True)
    pfos = fields.Nested(PoligrafSchema, many=True)
    invs = fields.Nested(InvestigationSchema, many=True)
    inquiries = fields.Nested(InquirySchema, many=True)
        