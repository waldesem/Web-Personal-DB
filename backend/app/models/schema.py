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
    """ Create model for relation"""
    class Meta:
        model = Relation
        ordered = True


class DocumentSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for document"""
    class Meta:
        model = Document
        ordered = True


class AddressSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for address"""
    class Meta:
        model = Address
        ordered = True


class StaffSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for staff"""
    class Meta:
        model = Staff
        ordered = True


class WorkplaceSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for workplace"""
    class Meta:
        model = Workplace
        ordered = True


class ContactSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for contact"""
    class Meta:
        model = Contact
        ordered = True


class AnketaSchema(ma.SQLAlchemySchema):
    """ Create schema for sending anketa"""

    resume = PersonSchema()
    document = DocumentSchema()
    address = AddressSchema()


class CheckSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for check"""
    class Meta:
        model = Check
        ordered = True
        

class InvestigationSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for investigation"""
    class Meta:
        model = Investigation
        ordered = True


class InquirySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inquiry
        ordered = True


class PoligrafSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for poligraf"""
    class Meta:
        model = Poligraf
        ordered = True


class RegistrySchema(ma.SQLAlchemyAutoSchema):
    """ Create schema for registry"""
    class Meta:
        model = Registry
        ordered = True


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
        

# Schemas for api endpoint '/api/v1/anketa'
class PersonSchemaApi(ma.SQLAlchemyAutoSchema):
    """ Create schema for person"""
    region_id = ma.auto_field()

    class Meta:
        model = Person
        ordered = True
        excude = ('region_id', 'category', 'addition', 'path', 'status', 'create', 'update', 'request_id')


class DocumentSchemaApi(ma.SQLAlchemyAutoSchema):
    """ Create schema for document"""
    class Meta:
        model = Document
        ordered = True
        excude = ('id',)


class AddressSchemaApi(ma.SQLAlchemyAutoSchema):
    """ Create schema for address"""
    class Meta:
        model = Address
        ordered = True
        excude = ('id',)


class StaffSchemaApi(ma.SQLAlchemyAutoSchema):
    """ Create schema for staff"""
    class Meta:
        model = Staff
        ordered = True
        excude = ('id',)


class WorkplaceSchemaApi(ma.SQLAlchemyAutoSchema):
    """ Create schema for workplace"""
    class Meta:
        model = Workplace
        ordered = True
        excude = ('id',)


class ContactSchemaApi(ma.SQLAlchemyAutoSchema):
    """ Create schema for contact"""
    class Meta:
        model = Contact
        ordered = True
        excude = ('id',)


class AnketaSchemaApi(ma.SQLAlchemySchema):
    """ Create schema to get resume from API"""

    resume = fields.Nested(PersonSchemaApi())
    document = fields.Nested(DocumentSchemaApi())
    staff = fields.Nested(StaffSchemaApi())
    addresses = fields.List(fields.Nested(AddressSchemaApi()))
    workplaces = fields.List(fields.Nested(WorkplaceSchemaApi()))
    contacts = fields.List(fields.Nested(ContactSchemaApi()))


# Schema for api endpoint '/api/v1/check'
class CheckSchemaApi(ma.SQLAlchemyAutoSchema):
    """ Create model for api check"""
    class Meta:
        model = Check
        ordered = True
        exclude = ('pfo', 'comments', 'conclusion', 'officer', 'deadline')