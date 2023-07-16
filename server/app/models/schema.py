from apiflask import Schema
from flask_marshmallow import Marshmallow
from marshmallow import fields

from ..models.model import User, Candidate, Staff, Document, Address, Contact, Workplace, \
    Check, Registry, Poligraf, Investigation, Inquiry, Message, Log

ma = Marshmallow()

class LogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Log
        ordered = True
        many = True
        

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
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
        model = Message
        ordered = True


class MessagesSchema(ma.SQLAlchemySchema):
    """ Create model for messages list"""
    
    messages = fields.Nested(MessageSchema, many=True)


class CandidateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Candidate
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
    """ Create model for sending anketa on check"""

    resume = CandidateSchema()
    document = DocumentSchema()
    address = AddressSchema()


class ResumeSchema(ma.SQLAlchemySchema):
    """ Create model for getting resume from API"""

    resume = fields.Nested(CandidateSchema())
    document = fields.Nested(DocumentSchema())
    staff = fields.Nested(StaffSchema())
    addresses = fields.List(fields.Nested(AddressSchema()))
    workplaces = fields.List(fields.Nested(WorkplaceSchema()))
    contacts = fields.List(fields.Nested(ContactSchema()))


class ProfileSchema(ma.SQLAlchemySchema):
    """ Create model for rendering profile"""

    resume = fields.Nested(CandidateSchema, many=True)
    documents = fields.Nested(DocumentSchema, many=True)
    addresses = fields.Nested(AddressSchema, many=True)
    contacts = fields.Nested(ContactSchema, many=True)
    workplaces = fields.Nested(WorkplaceSchema, many=True)
    staffs = fields.Nested(StaffSchema, many=True)
    checks = fields.Nested(CheckSchema, many=True)
    registries = fields.Nested(RegistrySchema, many=True)
    pfos = fields.Nested(PoligrafSchema, many=True)
    invs = fields.Nested(InvestigationSchema, many=True)
    inquiries = fields.Nested(InquirySchema, many=True)
        