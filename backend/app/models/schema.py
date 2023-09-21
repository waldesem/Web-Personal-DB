from apiflask import Schema
from marshmallow import fields

from .. import ma
from ..models.model import Relation, User, Person, Staff, Document, Address, Contact, Workplace, \
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


class UsersSchema(ma.SQLAlchemySchema):
        
    users = fields.Nested(UserSchema, many=True)
    

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


class RelationsSchema(ma.SQLAlchemySchema):
        
    relations = fields.Nested(RelationSchema, many=True)


class DocumentSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for document"""
    class Meta:
        model = Document
        ordered = True


class DocumentsSchema(ma.SQLAlchemySchema):
        
    documents = fields.Nested(DocumentSchema, many=True)


class AddressSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for address"""
    class Meta:
        model = Address
        ordered = True


class AddressesSchema(ma.SQLAlchemySchema):
        
    adresses = fields.Nested(AddressSchema, many=True)


class StaffSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for staff"""
    class Meta:
        model = Staff
        ordered = True


class StaffsSchema(ma.SQLAlchemySchema):
        
    staffs = fields.Nested(StaffSchema, many=True)


class WorkplaceSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for workplace"""
    class Meta:
        model = Workplace
        ordered = True


class WorkplacesSchema(ma.SQLAlchemySchema):
        
    workplaces = fields.Nested(WorkplaceSchema, many=True)


class ContactSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for contact"""
    class Meta:
        model = Contact
        ordered = True


class ContactsSchema(ma.SQLAlchemySchema):
        
    contacts = fields.Nested(ContactSchema, many=True)


class RelationSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for relation"""
    class Meta:
        model = Relation
        ordered = True


class RelationsSchema(ma.SQLAlchemySchema):
        
    relations = fields.Nested(RelationSchema, many=True)


class CheckSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for check"""
    class Meta:
        model = Check
        ordered = True


class ChecksSchema(ma.SQLAlchemySchema):
        
    check = fields.Nested(CheckSchema, many=True)


class RegistrySchema(ma.SQLAlchemyAutoSchema):
    """ Create schema for registry"""
    class Meta:
        model = Registry
        ordered = True


class RegistriesSchema(ma.SQLAlchemySchema):
        
    registries = fields.Nested(RegistrySchema, many=True)


class InquirySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inquiry
        ordered = True


class InquiriesSchema(ma.SQLAlchemySchema):
        
    inquries = fields.Nested(InquirySchema, many=True)


class InvestigationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Investigation
        ordered = True


class InvestigationsSchema(ma.SQLAlchemySchema):
        
    investigation = fields.Nested(InvestigationSchema, many=True)


class PoligrafSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for poligraf"""
    class Meta:
        model = Poligraf
        ordered = True


class PoligrafsSchema(ma.SQLAlchemySchema):
        
    poligrafs = fields.Nested(PoligrafSchema, many=True)


class ConnectSchema(ma.SQLAlchemyAutoSchema):
    """ Create schema for Connections """
    class Meta:
        model = Connect
        ordered = True


class ConnectsSchema(ma.SQLAlchemySchema):
    
    messages = fields.Nested(ConnectSchema, many=True)


# Schemas for Robot api endpoint
class AnketaSchema(ma.SQLAlchemySchema):
    """ Create schema for sending anketa"""
    resume = PersonSchema()
    document = DocumentSchema()
    address = AddressSchema()


# Schemas for api endpoint '/api/v1/anketa'
class AnketaSchemaApi(ma.SQLAlchemySchema):
    """ Create schema to get resume from API"""
    resume = fields.Nested(PersonSchema(), exclude = ('region_id', 'addition', 'path', 
                                                         'status', 'create', 'update', 'request_id',))
    document = fields.Nested(DocumentSchema(), exclude=('id',))
    staff = fields.Nested(StaffSchema(), exclude=('id',))
    addresses = fields.List(fields.Nested(AddressSchema(), exclude=('id',)))
    workplaces = fields.List(fields.Nested(WorkplaceSchema(), exclude=('id',)))
    contacts = fields.List(fields.Nested(ContactSchema(), exclude=('id',)))


# Schema for api endpoint '/api/v1/check
class CheckSchemaApi(ma.SQLAlchemyAutoSchema):
    """ Create schema for check API """
    class Meta:
        model = Check
        ordered = True
        exclude = ('pfo', 'comments', 'conclusion', 'officer', 'deadline',)
