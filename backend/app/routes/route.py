from datetime import datetime
import json
import os
import requests
import shutil

from apiflask import abort, EmptySchema
from flask import request, current_app
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import extract, func
from werkzeug.utils import secure_filename
from PIL import Image

from . import bp
from .. import db
from . login import r_g
from ..utils.utilities import ExcelFile, add_resume, create_folders
from ..models.model import User, Person, Staff, Document, Address, Contact, \
    Workplace, Check, Registry, Poligraf, Investigation, Inquiry, Relation, \
    Status, Report
from ..models.schema import RelationSchema, StaffSchema, AddressSchema, \
    PersonSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
    InvestigationSchema, PoligrafSchema, RegistrySchema, AnketaSchema,\
    WorkplaceSchema, ProfileSchema
from ..models.classes import Category, Roles, Groups, Status


class IndexView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def __init__(self) -> None:
        self.pagination = 16
        self.location_id = db.session.query(User.region_id).\
            filter_by(username=current_user.username).scalar()
        self.schema = PersonSchema()
    
    def post(self, flag, page):
        json_data = request.get_json()
        if flag == 'main' and self.location_id == 1:
            query = db.session.query(Person).order_by(Person.id.desc()). \
                paginate(page=page, 
                            per_page=self.pagination, 
                            error_out=False)
        elif flag == 'main' and self.location_id != 1:
            query = db.session.query(Person).\
                filter_by(region_id=self.location_id).\
                order_by(Person.id.desc()).paginate(page=page, 
                                                    per_page=self.pagination, 
                                                    error_out=False)
        elif flag == 'new':
            query = db.session.query(Person).\
                    filter(Person.status.in_([Status.new.value, 
                                                Status.update.value, 
                                                Status.repeat.value]), 
                            Person.region_id == self.location_id, 
                            Person.category == Category.candidate.value).\
                    order_by(Person.id.desc()).paginate(page=page, 
                                                        per_page=self.pagination, 
                                                        error_out=False)
        elif flag == 'officer': 
            query = db.session.query(Person).\
                filter(Person.status.notin_([Status.finish.value, 
                                                Status.result.value, 
                                                Status.cancel.value])). \
                join(Check, isouter=True).filter_by(officer=current_user.fullname).\
                order_by(Person.id.asc()).paginate(page=page, 
                                                   per_page=self.pagination, 
                                                   error_out=False)
        elif flag == 'search' and self.location_id == 1:
            query = db.session.query(Person).\
                filter(Person.fullname.ilike('%{}%'.format(json_data['fullname']))).\
                order_by(Person.id.asc()).paginate(page=page, 
                                                   per_page=self.pagination, 
                                                   error_out=False)
        elif flag == 'search' and self.location_id != 1:
            query = db.session.query(Person).\
                filter(Person.fullname.ilike('%{}%'.format(json_data['fullname'])), 
                       Person.region_id == self.location_id).\
                order_by(Person.id.asc()).paginate(page=page, 
                                                   per_page=self.pagination, 
                                                   error_out=False)
            
        has_next, has_prev = int(query.has_next), int(query.has_prev)
        return [self.schema.dump(query, many=True), 
                {'has_next': has_next, "has_prev": has_prev}]

bp.add_url_rule('/index/<flag>/<int:page>', 
                view_func=IndexView.as_view('index'))


class ProfileView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(ProfileSchema)
    def get(self, action, itemm_id):
        resume = db.session.query(Person).get(itemm_id)
        staffs, docs, addrs, conts, works, rels, checks, regs, pfos, invs, inqs = \
            [db.session.query(model).filter_by(person_id=itemm_id).all() 
                 for model in [Staff, Document, Address, Contact, Workplace, 
                               Relation, Check, Registry, Poligraf, 
                               Investigation, Inquiry]]
        return {'resume': resume, 
                'staffs': staffs, 
                'documents': docs, 
                'addresses': addrs, 
                'contacts': conts, 
                'workplaces': works, 
                'relations': rels, 
                'checks': checks, 
                'registries': regs, 
                'pfos': pfos, 'invs': invs, 
                'inquiries': inqs}
    
bp.add_url_rule('/profile/<action>/<int:itemm_id>>', 
                view_func=ProfileView.as_view('profile'))


class ResumeView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(PersonSchema)
    def get(self, action, person_id):
        person = db.session.query(Person).get(person_id)
        if action == 'status':
            person.status = Status.update.value
            db.session.commit()
            return db.session.query(Person).get(person_id)
        elif action == 'send':
            if person.has_status([Status.new.value, 
                                  Status.update.value, 
                                  Status.repeat.value]):
                anketa_schema = AnketaSchema()
                serial = anketa_schema.dump(dict(
                    resume = person, 
                    document = db.session.query(Document).\
                        filter_by(person_id=person_id).\
                        order_by(Document.id.desc()).first(), 
                    address = db.session.query(Address).\
                        filter(Address.person_id==person_id, 
                               Address.view.ilike("%регистрац%")).\
                        order_by(Address.id.desc()).first()))
                try:
                    response = requests.post(url='https://httpbin.org/post', 
                                             json=serial, 
                                             timeout=5)
                    response.raise_for_status()
                    if response.status_code == 200:
                        check_path = create_folders(person_id, 
                                                    person.fullname, 
                                                    'check')
                        person.status = Status.robot.value
                        db.session.add(Check(officer=current_user.fullname, 
                                             path=check_path,
                                             person_id = person_id))
                        db.session.commit()
                        return db.session.query(Person).get(person_id)
                    return abort(response.status_code)
                except requests.exceptions.RequestException as e:
                    print(e)
            return abort(404)
        return person
        
    @r_g.roles_required(Roles.user.name, Roles.api.name)
    @bp.input(PersonSchema)
    def post(self, action, json_data):
        location_id = db.session.query(User.region_id).\
            filter_by(username=current_user.username).scalar()
        person_id = add_resume(json_data, location_id, action)
        return {'message': person_id}
    
    @r_g.roles_required(Roles.user.name)
    @bp.input(PersonSchema)
    def patch(self, action, person_id, json_data):
        person = db.session.query(Person).get(person_id)
        person.region_id = json_data['region_id']
        users = db.session.query(User).\
            filter_by(region_id=json_data['region_id']).all()
        if len(users):
            for user in users:
                db.session.add(Report(report=f'Делегирована анкета ID #{id} \
                                  от {current_user.username}', user_id=user.id))
        db.session.commit()
        return '', 201
        
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, person_id):
        person = db.session.query(Person).get(person_id)
        try:
            shutil.rmtree(person.path)
        except Exception as e:
            print(e)
        db.session.delete(person)
        db.session.commit()
        return ''
    
resume_view = ResumeView.as_view('resume')
bp.add_url_rule('/resume/<action>', 
                view_func=resume_view, methods=['POST'])
bp.add_url_rule('/resume/<action>/<int:person_id>', 
                view_func=resume_view, methods=['GET', 'PATCH', 'DELETE'])


class StaffView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def get(self, action, item_id):
        schema = StaffSchema()
        return schema.dump(db.session.query(Staff).\
                           filter_by(person_id=item_id).\
                            order_by(Staff.id.asc()).all(), many=True)

    @bp.input(StaffSchema)
    @r_g.roles_required(Roles.user.value)
    def post(self, action, item_id, json_data):
        db.session.add(Staff(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201
        
    @bp.input(StaffSchema)
    @r_g.roles_required(Roles.user.value)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Staff).get(item_id), k, v)
        db.session.commit()
        return '', 201
   
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Staff).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/staff/<action>/<int:item_id>', 
                view_func=StaffView.as_view('staff'))


class DocumentView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def get(self, action, item_id):
        schema = DocumentSchema()
        return schema.dump(db.session.query(Document).\
                           filter_by(person_id=item_id).\
                            order_by(Document.id.asc()).all(), many=True)
    
    @r_g.roles_required(Roles.user.value)
    @bp.input(DocumentSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Document(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201
        
    @r_g.roles_required(Roles.user.value)
    @bp.input(DocumentSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Document).get(item_id), k, v)
        db.session.commit()
        return '', 201
   
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Document).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/document/<action>/<int:item_id>', 
                view_func=DocumentView.as_view('document'))


class AddressView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def get(self, action, item_id):
        schema = AddressSchema()
        return schema.dump(db.session.query(Address).\
                           filter_by(person_id=item_id).\
                            order_by(Address.id.asc()).all(), many=True)
            
    @r_g.roles_required(Roles.user.value)
    @bp.input(AddressSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Address(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201
        
    @r_g.roles_required(Roles.user.value)    
    @bp.input(AddressSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Address).get(item_id), k, v)
        db.session.commit()
        return '', 201
   
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Address).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/address/<action>/<int:item_id>', 
                view_func=AddressView.as_view('address'))


class ContactView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def get(self, action, item_id):
        schema = ContactSchema()
        return schema.dump(db.session.query(Contact).\
                           filter_by(person_id=item_id).\
                            order_by(Contact.id.asc()).all(), many=True)
            
    @r_g.roles_required(Roles.user.value)
    @bp.input(ContactSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Contact(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201
        
    @r_g.roles_required(Roles.user.value)
    @bp.input(ContactSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Contact).get(item_id), k, v)
        db.session.commit()
        return '', 201
   
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Contact).get(item_id))
        db.session.commit()
        return ''

bp.add_url_rule('/contact/<action>/<int:item_id>', 
                view_func=ContactView.as_view('contact'))


class WorkplaceView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def get(self, action, item_id):
        schema = WorkplaceSchema()
        return schema.dump(db.session.query(Workplace).\
                           filter_by(person_id=item_id).\
                            order_by(Workplace.id.asc()).all(), many=True)
            
    @r_g.roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    def post(self, action, item_id, json_data):
        json_data['now_work'] = bool(json_data.pop('now_work')) if 'now_work' in json_data else False
        db.session.add(Workplace(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201
        
    @r_g.roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    def patch(self, action, item_id, json_data):
        json_data['now_work'] = bool(json_data.pop('now_work')) if 'now_work' in json_data else False
        for k, v in json_data.items():
            setattr(db.session.query(Workplace).get(item_id), k, v)
        db.session.commit()
        return '', 201
   
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Workplace).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/workplace/<action>/<int:item_id>', 
                view_func=WorkplaceView.as_view('workplace'))


class RelationView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def get(self, action, item_id):
        schema = RelationSchema()
        return schema.dump(db.session.query(Relation).\
                           filter_by(person_id=item_id).\
                            order_by(Relation.id.asc()).all(), many=True)
            
    @r_g.roles_required(Roles.user.value)
    @bp.input(RelationSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Relation(**json_data | {'person_id': item_id}))
        db.session.add(Relation(relation = json_data['relation'], 
                                relation_id = item_id,
                                person_id = json_data['relation_id']))
        db.session.commit()
        return '', 201
        
    @r_g.roles_required(Roles.user.value)
    @bp.input(RelationSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Relation).get(item_id), k, v)
        db.session.commit()
        return '', 201
   
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Relation).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/relation/<action>/<int:item_id>', 
                view_func=RelationView.as_view('relation'))


class CheckView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def get(self, action, item_id):
        if action == 'add':
            person = db.session.query(Person).get(item_id)
            if person.has_status([Status.new.value, 
                                  Status.update.value, 
                                  Status.repeat.value]):
                check_path = create_folders(item_id, person.fullname, 'check')
                person.status = Status.manual.value
                db.session.add(Check(officer=current_user.fullname, 
                                        path = check_path,
                                        person_id = item_id))
                db.session.commit()
                return '', 201
        
        if action == 'self':
            check = db.session.query(Check).get(item_id)
            prev_officer = db.session.query(User).filter_by(fullname=check.officer).one_or_none()
            new_officer = db.session.query(User).filter_by(fullname=current_user.fullname).one_or_none()
            db.session.add(Report(report=f'Aнкета ID #{id} делегирована \
                                  {current_user.fullname}', user_id=prev_officer.id))
            check.officer = current_user.fullname
            db.session.add(Report(report=f'Aнкета ID #{id} переделегирована \
                                  {current_user.fullname}', user_id=new_officer.id))
            db.session.commit()
            return '', 201
                
        schema = CheckSchema()
        return schema.dump(db.session.query(Check).\
                           filter_by(person_id=item_id).\
                            order_by(Check.id.asc()).all(), many=True)
            
    @r_g.roles_required(Roles.user.value)
    @bp.input(CheckSchema)
    def patch(self, action, item_id, json_data):
        json_data['pfo'] = bool(json_data.pop('pfo')) if 'pfo' in json_data else False
        if action == 'create':
            person = db.session.query(Person).get(item_id)        
            db.session.add(Check(**json_data | {'person_id': item_id, 
                                                'officer': current_user.fullname}))
        else:
            check = db.session.query(Check).get(item_id)
            person = db.session.query(Person).get(check.person_id)
            for k, v in json_data.items():
                setattr(check, k, v)
        if json_data['conclusion'] == (Status.save.value).upper():
            person.status = Status.save.value
        else:
            person.status = Status.poligraf.value if json_data['pfo'] \
                else Status.result.value
        db.session.commit()    
        return '', 201
   
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        check = db.session.query(Check).get(item_id)
        try:
            shutil.rmtree(check.path)
        except Exception as e:
            print(e)
        person = db.session.query(Person).get(db.session.query(Check.person_id).\
                                              filter_by(id=item_id).one_or_none())
        person.status = Status.update.value
        db.session.delete(check)
        db.session.commit()
        return ''
    
bp.add_url_rule('/check/<action>/<int:item_id>', 
                view_func=CheckView.as_view('check'))


class RegistryView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def add_to_db(self, query, item, check_id, person_id):
        db.session.add(Registry(**item | {'check_id': check_id,
                                          'person_id': person_id}))
        query.status = Status.cancel.value \
            if item['decision'] == Status.cancel.value \
                else Status.finish.value
        db.session.commit()
        
    def get(self, action, item_id):
        schema = RegistrySchema()
        return schema.dump(db.session.query(Registry).\
                           filter_by(person_id=item_id).\
                            order_by(Registry.id.asc()).all(), many=True)
    
    @r_g.roles_required(Roles.superuser.value)
    @bp.input(RegistrySchema)
    def post(self, action, item_id, json_data):
        check_id = db.session.query(Check.id).filter_by(person_id=item_id).\
            order_by(Check.id.desc()).scalar()
        reg = {'supervisor': current_user.fullname} | json_data
        person = db.session.query(Person).get(item_id)
        if person.request_id and person.request_id != 'NULL':  
            try:
                response = requests.post(url='https://httpbin.org/post', 
                                        json=json.dumps({"id": person.request_id}
                                                        | reg), timeout=5)
                response.raise_for_status()
                if response.status_code == 200:
                    self.add_to_db(person, reg, check_id, item_id)
                    return '', 201
                else:
                    return '', response.status_code
            except Exception as e:
                print(e)
                return '', 404
        self.add_to_db(person, reg, check_id, item_id)
        return '', 201

bp.add_url_rule('/registry/<action>/<int:item_id>', 
                view_func=RegistryView.as_view('registry'))


class InvestigationView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def get(self, action, item_id):
        schema = InvestigationSchema()
        return schema.dump(db.session.query(Investigation).\
                           filter_by(person_id=item_id).\
                            order_by(Investigation.id.asc()).all(), many=True)
    
    @r_g.roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Investigation(**json_data | {'person_id': item_id, 
                                                    'officer': current_user.fullname}))
        db.session.commit()
        return '', 201
        
    @r_g.roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    def patch(self, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Investigation).get(item_id), k, v)
        db.session.commit()
        return '', 201
   
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        invs = db.session.query(Investigation).get(item_id)
        db.session.delete(invs)
        try:
            shutil.rmtree(invs.path)
        except Exception as e:
            print(e)
        db.session.commit()
        return ''
    
bp.add_url_rule('/investigation/<action>/<int:item_id>', 
                view_func=InvestigationView.as_view('investigation'))


class PoligrafView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]

    def get(self, action, item_id):
        schema = PoligrafSchema()
        return schema.dump(db.session.query(Poligraf).\
                           filter_by(person_id=item_id).\
                            order_by(Poligraf.id.asc()).all(), many=True)
    
    @r_g.roles_required(Roles.user.value)
    @bp.input(PoligrafSchema)
    def post(self, action, item_id, json_data):
        person = db.session.query(Person).get(item_id)
        if person.has_status(Status.poligraf.value):
            person.status = Status.result.value
        db.session.add(Poligraf(**json_data | {'person_id': item_id, 
                                               'officer': current_user.fullname}))
        db.session.commit()
        return '', 201
        
    @r_g.roles_required(Roles.user.value)
    @bp.input(PoligrafSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Poligraf).get(item_id), k, v)
        db.session.commit()
        return '', 201
   
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Poligraf).get(item_id))
        db.session.commit()
        return ''
        
bp.add_url_rule('/poligraf/<action>/<int:item_id>', 
                view_func=PoligrafView.as_view('poligraf'))


class InquiryView(MethodView):
    
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def get(self, action, item_id):
        schema = InquirySchema()
        return schema.dump(db.session.query(Inquiry).\
                           filter_by(person_id=item_id).\
                            order_by(Inquiry.id.asc()).all(), many=True)
    
    @bp.input(InquirySchema)
    @r_g.roles_required(Roles.user.value)
    def post(self, action, item_id, json_data):
        db.session.add(Inquiry(**json_data | {'person_id': item_id, 
                                              'officer': current_user.fullname}))
        db.session.commit()
        return '', 201
        
    @bp.input(InquirySchema)
    @r_g.roles_required(Roles.user.value)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Inquiry).get(item_id), k, v)
        db.session.commit()
        return '', 201
   
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Inquiry).get(item_id))
        db.session.commit()
        return ''

bp.add_url_rule('/inquiry/<action>/<int:item_id>', 
                view_func=InquiryView.as_view('inquiry'))


class FileView(MethodView):

    decorators = [r_g.group_required(Groups.staffsec.name), 
                  r_g.roles_required(Roles.user.name),
                  bp.doc(hide=True)]

    def post(self, action, item_id=0):
        
        if request.files['file'].filename == '':
            return {'result': False, 'item_id': item_id}
        
        if action == 'anketa':
            file = request.files['file']
            
            filename = secure_filename(file.filename)
            temp_path = os.path.join(current_app.config["BASE_PATH"], 
                                     f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}\
                                        -{filename}')
            file.save(temp_path)
            
            excel = ExcelFile(temp_path)
            excel.close()
            location_id = db.session.query(User.region_id).\
                filter_by(username=current_user.username).scalar()

            person_id = add_resume(excel.resume, location_id, 'create')

            models = [Staff, Document, Address, Contact, Workplace]
            for count, items in enumerate([excel.staff, excel.passport, 
                                   excel.addresses, excel.contacts, 
                                   excel.workplaces]):
                for item in items:
                    if item:
                        print(item)
                        db.session.add(models[count](**item | 
                                                     {'person_id': person_id}))
            db.session.commit()

            person = db.session.query(Person).get(person_id)
            if person.path:
                if not os.path.isdir(person.path):
                    os.mkdir(os.path.join(person.path))
                new_path = person.path
                db.session.commit()
            else:
                new_path = os.path.join(current_app.config["BASE_PATH"], 
                                        f'{person_id}-{person.fullname}')
                person.path = new_path
                db.session.commit()
                if not os.path.isdir(new_path):
                    os.mkdir(new_path)
                person.path = new_path
                db.session.commit()

            action_folder = create_folders(person_id, person.fullname, action)

            save_path = os.path.join(action_folder, filename)
            if not os.path.isfile(save_path):
                shutil.move(temp_path, save_path)
            return {'message': person_id}

        else:
            model_mapping = {
                'check': Check,
                'investigation': Investigation,
                'poligraf': Poligraf,
                'inquiry': Inquiry,
                'image': Person
            }
            files = request.files.getlist('file')
            model = model_mapping.get(action)
            item = db.session.query(model).filter_by(id=item_id).scalar()
            folder = item.path
            if not folder:
                person = db.session.query(Person).get(item.person_id)
                folder = create_folders(person.id, person.fullname, action)
                item.path = folder
                db.session.commit()
            if action == 'image':
                im = Image.open(files[0])
                rgb_im = im.convert('RGB')
                images = os.path.join(folder, 'images')
                if not os.path.isdir(images):
                    os.mkdir(images)
                image_path = os.path.join(images, 'image.jpg')
                if image_path:
                    os.remove(image_path)
                rgb_im.save(os.path.join(image_path))
            else:
                for file in files:
                    filename = secure_filename(file.filename)
                    for file in files:
                        file.save(os.path.join(folder, 
                            f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}-{filename}'))
            return '', 201
        

    @r_g.group_required(Groups.staffsec.name)
    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        person = db.session.query(Person).get(item_id)
        os.remove(person.path)
        person.path = ''
        db.session.commit()
        return ''

bp.add_url_rule('/file/<action>/<int:item_id>', 
                view_func=FileView.as_view('file'))


class InfoView(MethodView):

    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def post(self):
        response = request.get_json()
        
        candidates = db.session.query(
                extract('month', Registry.deadline).label('month'),
                Registry.decision, 
                func.count(Registry.id)
            ).\
            join(Check, Check.id == Registry.check_id). \
            join(Person, Person.id == Check.person_id).\
            group_by(Registry.decision).\
            filter(Registry.deadline.between(response['start'], response['end']),
                   Person.region_id == int(response['region'])).all()
    
        pfo = db.session.query(
                extract('month', Registry.deadline).label('month'),
                Poligraf.theme, 
                func.count(Poligraf.id)).\
            group_by(Poligraf.theme).\
            filter(Poligraf.deadline.between(response['start'], 
                                             response['end'])).all()
        
        return {"candidates": [
                    {'month': row[0], 'decision': row[1], 'count': row[2]}
            for row in candidates
            ],
                "poligraf": [
                    {'month': row[0], 'decision': row[1], 'count': row[2]}
            for row in pfo
            ]}

bp.add_url_rule('/information', view_func=InfoView.as_view('information'))