from apiflask import Schema
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemySchema

from .. import ma
from ..models.model import Category, Conclusion, Relation, Status, User, Person, \
    Affilation, Staff, Document, Address, Contact, Workplace, Check, Poligraf, \
    Investigation, Inquiry, Message, Region, Role, Group, Connect


class RoleSchema(SQLAlchemyAutoSchema):
    """ Create model for role"""
    class Meta:
        model = Role
        ordered = True


class GroupSchema(SQLAlchemyAutoSchema):
    """ Create model for group"""
    class Meta:
        model = Group
        ordered = True
        

class UserSchema(SQLAlchemyAutoSchema):
    """ Create model for user"""
    roles = ma.Nested('RoleSchema', many=True)
    groups = ma.Nested('GroupSchema', many=True)

    class Meta:
        model = User
        ordered = True
        include_fk = True


class LoginSchema(Schema):
    """ Create model for login"""
    username = fields.String()
    password = fields.String()

 
class PasswordSchema(LoginSchema):
    """ Create model for login"""
    new_pswd = fields.String()
    conf_pswd = fields.String()
 

class MessageSchema(SQLAlchemyAutoSchema):
    """ Create model for message"""
    class Meta:
        model = Message
        ordered = True


class PersonSchema(SQLAlchemyAutoSchema):
    """ Create model for person"""

    class Meta:
        model = Person
        ordered = True
        include_fk = True
        exclude = ('search_vector',)
        

class RegionSchema(SQLAlchemyAutoSchema):
    """ Create model for location"""
    class Meta:
        model = Region 
        ordered = True


class CategorySchema(SQLAlchemyAutoSchema):
    """ Create model for category"""
    class Meta:
        model = Category 
        ordered = True


class StatusSchema(SQLAlchemyAutoSchema):
    """ Create model for status"""
    class Meta:
        model = Status 
        ordered = True


class RelationSchema(SQLAlchemyAutoSchema):
    """ Create model for relation"""
    class Meta:
        model = Relation
        ordered = True


class DocumentSchema(SQLAlchemyAutoSchema):
    """ Create model for document"""
    class Meta:
        model = Document
        ordered = True
        exclude = ('search_vector',)

class AddressSchema(SQLAlchemyAutoSchema):
    """ Create model for address"""
    class Meta:
        model = Address
        ordered = True


class StaffSchema(SQLAlchemyAutoSchema):
    """ Create model for staff"""
    class Meta:
        model = Staff
        ordered = True


class WorkplaceSchema(SQLAlchemyAutoSchema):
    """ Create model for workplace"""
    class Meta:
        model = Workplace
        ordered = True


class ContactSchema(SQLAlchemyAutoSchema):
    """ Create model for contact"""
    class Meta:
        model = Contact
        ordered = True


class AffilationSchema(SQLAlchemyAutoSchema):
    """ Create model for affilation"""
    class Meta:
        model = Affilation
        ordered = True


class CheckSchema(SQLAlchemyAutoSchema):
    """ Create model for check"""
    class Meta:
        model = Check
        ordered = True


class ConclusionSchema(SQLAlchemyAutoSchema):
    """ Create model for conclusion"""
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
    """ Create model for poligraf"""
    class Meta:
        model = Poligraf
        ordered = True


class ConnectSchema(SQLAlchemyAutoSchema):
    """ Create schema for Connections """
    class Meta:
        model = Connect
        ordered = True
        exclude = ('search_vector',)


class AnketaSchemaApi(SQLAlchemySchema):
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


class CheckSchemaApi(SQLAlchemySchema):
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


class Pagination:

    def __init__ (self, query, pagination, page):
        self.query = query.all()
        self.pagination = pagination 
        self.page = page
        self.start_index = self.pagination*(self.page-1)
        self.end_index = self.pagination*self.page
        self.results = self.query[self.start_index:self.end_index]
        
    def paginate (self):
        if self.page:
            return self.results
    
    def has_prev(self):
        if self.page < 2:
            return False
        prev_items = self.query[self.start_index-1:self.end_index]
        return True if len(self.results) < len(prev_items) else False

    def has_next(self):
        next_items = self.query[self.start_index:self.end_index+1]
        return True if len(self.results) < len(next_items) else False

