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
 

class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        ordered = True
        many = True 

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
    class Meta:
        resume = CandidateSchema()
        document = DocumentSchema()
        address = AddressSchema()


class ResumeSchema(ma.SQLAlchemySchema):
    class Meta:
        resume = fields.Nested(CandidateSchema())
        document = fields.Nested(DocumentSchema())
        staff = fields.Nested(StaffSchema())
        addresses = fields.List(fields.Nested(AddressSchema()))
        workplaces = fields.List(fields.Nested(WorkplaceSchema()))
        contacts = fields.List(fields.Nested(ContactSchema()))


class ProfileSchema(ma.SQLAlchemySchema):
    class Meta:
        resume = fields.List(fields.Nested(CandidateSchema))
        documents = fields.List(fields.Nested(DocumentSchema))
        addresses = fields.List(fields.Nested(AddressSchema))
        contacts = fields.List(fields.Nested(ContactSchema))
        workplaces = fields.List(fields.Nested(WorkplaceSchema))
        staffs = fields.List(fields.Nested(StaffSchema))
        checks = fields.List(fields.Nested(CheckSchema))
        registries = fields.List(fields.Nested(RegistrySchema))
        pfos = fields.List(fields.Nested(PoligrafSchema))
        invs = fields.List(fields.Nested(InvestigationSchema))
        inquiries = fields.List(fields.Nested(InquirySchema))
        