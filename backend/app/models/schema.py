from apiflask import Schema
from marshmallow import fields

from .. import ma
from ..models.model import OneS, Relation, User, Person, Staff, Document, Address, Contact, Workplace, \
    Check, Registry, Poligraf, Investigation, Inquiry, Report, Region, Role, Group, Connect


class RoleSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for role"""
    class Meta:
        model = Role
        ordered = True


class GroupSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for group"""
    class Meta:
        model = Group
        ordered = True
        

class UserSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for user"""
    region_id = ma.auto_field()
    roles = ma.Nested('RoleSchema', many=True)
    groups = ma.Nested('GroupSchema', many=True)

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


class PersonSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for person"""
    region_id = ma.auto_field()

    class Meta:
        model = Person
        ordered = True
        exclude = ('search_vector',) # only if use searchable sqlalchemy
        

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


class CheckSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for check"""
    class Meta:
        model = Check
        ordered = True


class RegistrySchema(ma.SQLAlchemyAutoSchema):
    """ Create schema for registry"""
    class Meta:
        model = Registry
        ordered = True


class InquirySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inquiry
        ordered = True


class InvestigationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Investigation
        ordered = True


class PoligrafSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for poligraf"""
    class Meta:
        model = Poligraf
        ordered = True


class OneSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for 1C"""
    class Meta:
        model = OneS
        ordered = True


class ConnectSchema(ma.SQLAlchemyAutoSchema):
    """ Create schema for Connections """
    class Meta:
        model = Connect
        ordered = True
        exclude = ('search_vector',)


class AnketaSchema(ma.SQLAlchemySchema):
    """ Create schema for sending anketa"""
    resume = PersonSchema()
    document = DocumentSchema()
    address = AddressSchema()


class AnketaSchemaApi(ma.SQLAlchemySchema):
    """ Create schema to get anketa from /api/v1/anketa"""
    resume = fields.Nested(PersonSchema(), 
                           exclude = ('region_id', 'addition', 'path', 'status', 
                                      'create', 'update', 'request_id',))
    document = fields.List(fields.Nested(DocumentSchema(), exclude=('id',)))
    staff = fields.List(fields.Nested(StaffSchema(), exclude=('id',)))
    addresses = fields.List(fields.Nested(AddressSchema(), exclude=('id',)))
    workplaces = fields.List(fields.Nested(WorkplaceSchema(), exclude=('id',)))
    contacts = fields.List(fields.Nested(ContactSchema(), exclude=('id',)))


class CheckSchemaApi(ma.SQLAlchemyAutoSchema):
    """ Create schema for check /api/v1/check """
    class Meta:
        model = Check
        ordered = True
        exclude = ('workplace', 'internet', 'cronos', 'cros', 'addition', 
                   'pfo', 'comments', 'conclusion', 'officer', 'deadline',)


models_schemas = {
    'user': [User, UserSchema()],
    'role': [Role, RoleSchema()],
    'group': [Group, GroupSchema()],
    'report': [Report, MessageSchema()],
    'resume': [Person, PersonSchema()],
    'staff': [Staff, StaffSchema()],
    'document': [Document, DocumentSchema()],
    'address': [Address, AddressSchema()],
    'contact': [Contact, ContactSchema()],
    'workplace': [Workplace, WorkplaceSchema()],
    'relation': [Relation, RelationSchema()],
    'check': [Check, CheckSchema()],
    'registry': [Registry, RegistrySchema()],
    'poligraf': [Poligraf, PoligrafSchema()],
    'investigation': [Investigation, InvestigationSchema()],
    'inquiry': [Inquiry, InquirySchema()],
    'connect': [Connect, ConnectSchema],
    'ones': [OneS, OneSchema]
}