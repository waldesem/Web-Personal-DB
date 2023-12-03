from marshmallow import Schema, fields

from .. import ma
from ..models.model import Category, Conclusion, Relation, Status, User, Person, \
    Affilation, Staff, Document, Address, Contact, Workplace, Check, Poligraf, \
    Investigation, Inquiry, Message, Region, Role, Group, Connect


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


class LoginSchema(Schema):
    """ Create model for login"""
    username = fields.String()
    password = fields.String()

 
class PasswordSchema(LoginSchema):
    """ Create model for login"""
    new_pswd = fields.String()
    conf_pswd = fields.String()
 

class MessageSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for message"""
    class Meta:
        model = Message
        ordered = True


class PersonSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for person"""
    region_id = ma.auto_field()

    class Meta:
        model = Person
        ordered = True
        exclude = ('search_vector',)
        

class RegionSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for location"""
    class Meta:
        model = Region 
        ordered = True


class CategorySchema(ma.SQLAlchemyAutoSchema):
    """ Create model for category"""
    class Meta:
        model = Category 
        ordered = True


class StatusSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for status"""
    class Meta:
        model = Status 
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
        exclude = ('search_vector',)

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


class AffilationSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for affilation"""
    class Meta:
        model = Affilation
        ordered = True


class CheckSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for check"""
    class Meta:
        model = Check
        ordered = True


class ConclusionSchema(ma.SQLAlchemyAutoSchema):
    """ Create model for conclusion"""
    class Meta:
        model = Conclusion 
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


class ConnectSchema(ma.SQLAlchemyAutoSchema):
    """ Create schema for Connections """
    class Meta:
        model = Connect
        ordered = True
        exclude = ('search_vector',)


class AnketaSchemaApi(ma.SQLAlchemySchema):
    """ Create schema for sending anketa"""
    id = fields.String()
    fullname = fields.String()
    birthday = fields.String()
    birthplace = fields.String()
    snils = fields.String()
    inn = fields.String()
    series = fields.String()
    number = fields.String()
    agency = fields.String()
    issue = fields.String()
    address = fields.String()


class CheckSchemaApi(ma.SQLAlchemyAutoSchema):
    """ Create schema for check /api/v1/check """
    id = fields.String()
    employee = fields.String()
    document = fields.String()
    inn = fields.String()
    debt = fields.String()
    bankruptcy = fields.String()
    bki = fields.String()
    courts = fields.String()
    affiliation = fields.String()
    terrorist = fields.String()
    mvd = fields.String()
        

models_schemas = {
    'user': [User, UserSchema()],
    'role': [Role, RoleSchema()],
    'group': [Group, GroupSchema()],
    'message': [Message, MessageSchema()],
    'resume': [Person, PersonSchema()],
    'staff': [Staff, StaffSchema()],
    'document': [Document, DocumentSchema()],
    'address': [Address, AddressSchema()],
    'contact': [Contact, ContactSchema()],
    'workplace': [Workplace, WorkplaceSchema()],
    'relation': [Relation, RelationSchema()],
    'affilation': [Affilation, AffilationSchema()],
    'check': [Check, CheckSchema()],
    'poligraf': [Poligraf, PoligrafSchema()],
    'investigation': [Investigation, InvestigationSchema()],
    'inquiry': [Inquiry, InquirySchema()],
    'connect': [Connect, ConnectSchema]
    }