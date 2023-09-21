from datetime import datetime
import json
import os
import shutil
from apiflask import abort
import requests

from flask import request, current_app, send_from_directory
from flask.views import MethodView
from flask_jwt_extended import current_user, jwt_required
from sqlalchemy import func
from werkzeug.utils import secure_filename

from . import bp
from .. import db
from . login import roles_required, group_required
from ..utils.excel import ExcelFile
from ..utils.actions import resume_data, add_resume, create_folders
from ..models.model import User, Person, Staff, Document, Address, Contact, \
    Workplace, Check, Registry, Poligraf, Investigation, Inquiry, Relation, \
    Status, Report
from ..models.schema import AddressesSchema, ChecksSchema, ContactsSchema, \
    DocumentsSchema, InquiriesSchema, InvestigationsSchema, PoligrafsSchema, \
    RegistriesSchema, RelationSchema, RelationsSchema, StaffSchema, AddressSchema, \
    PersonSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
    InvestigationSchema, PoligrafSchema, RegistrySchema, StaffsSchema, \
    WorkplaceSchema, AnketaSchema, WorkplacesSchema
from ..models.classes import Category, Roles, Groups, Status


@bp.get('/', defaults={'path': ''})
@bp.get('/<path:path>')
@bp.doc(hide=True)
def main(path=''):
    """
    Get the file from the specified path in the static folder and return it, 
    or return the index.html file if the path is not found.
    """
    if path and os.path.exists(os.path.join(bp.static_folder, path)):
        return send_from_directory(bp.static_folder, path)
    else:
        return bp.send_static_file('index.html')


class IndexView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    def __init__(self) -> None:
        self.pagination = 16
        self.location_id = db.session.query(User.region_id).\
            filter_by(username=current_user.username).scalar()
        self.schema = PersonSchema()
    
    def get(self, flag, page):
        match flag:
            case 'main':
                if self.location_id == 1:
                    query = db.session.query(Person).order_by(Person.id.desc()). \
                        paginate(page=page, 
                                 per_page=self.pagination, 
                                 error_out=False)
                else:
                    query = db.session.query(Person).\
                        filter_by(region_id=self.location_id).\
                        order_by(Person.id.desc()).paginate(page=page, 
                                                            per_page=self.pagination, 
                                                            error_out=False)
            case 'new':
                if self.location_id == 1:
                    query = db.session.query(Person).\
                        filter(Person.status.in_([Status.new.value, 
                                                  Status.update.value, 
                                                  Status.repeat.value]), 
                               Person.region_id == self.location_id, 
                               Person.category == Category.candidate.value).\
                        order_by(Person.id.desc()).paginate(page=page, 
                                                            per_page=self.pagination, 
                                                            error_out=False)
                else:
                    query = db.session.query(Person).\
                        filter(Person.status.in_([Status.new.value, 
                                                  Status.update.value, 
                                                  Status.repeat.value]), 
                                Person.region_id == self.location_id, 
                                Person.category == Category.candidate.value).\
                        order_by(Person.id.desc()).paginate(page=page, 
                                                            per_page=self.pagination, 
                                                            error_out=False)
            case 'officer': 
                query = db.session.query(Person).\
                    filter(Person.status.notin_([Status.finish.value, 
                                                 Status.result.value, 
                                                 Status.cancel.value])). \
                    join(Check, isouter=True).filter_by(officer=current_user.username).\
                    order_by(Person.id.asc()).paginate(page=page, 
                                                       per_page=self.pagination, 
                                                       error_out=False)
        datas = self.schema.dump(query, many=True)
        has_next, has_prev = int(query.has_next), int(query.has_prev)
        return [datas, {'has_next': has_next, "has_prev": has_prev}]

    @input(PersonSchema)
    def post(self, page, json_data):
        if self.location_id == 1:
            query = db.session.query(Person).\
                filter(Person.fullname.ilike('%{}%'.format(json_data['fullname']))).\
                order_by(Person.id.asc()).paginate(page=page, 
                                                   per_page=self.pagination, 
                                                   error_out=False)
        else:
            query = db.session.query(Person).\
                filter(Person.fullname.ilike('%{}%'.format(json_data['fullname'])), 
                       Person.region_id == self.location_id).\
                order_by(Person.id.asc()).paginate(page=page, 
                                                   per_page=self.pagination, 
                                                   error_out=False)
        datas = self.schema.dump(query, many=True)
        has_next, has_prev = int(query.has_next), int(query.has_prev)
        return [datas, {'has_next': has_next, "has_prev": has_prev}]

index_view = IndexView.as_view('index')
bp.add_url_rule('/index/<flag>/<int:page>', view_func=index_view, methods=['GET'])
bp.add_url_rule('/index/<int:page>', view_func=index_view, methods=['POST'])


class ResumeView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(PersonSchema)
    def get(self, action, person_id):
        if action == 'status':
            person = db.session.query(Person).get(person_id)
            if person:
                person.status = Status.update.value
                db.session.commit()
                return db.session.query(Person).filter_by(id=person_id).one_or_none()
        elif action == 'send':
            resume = db.session.query(Person).get(person_id)
            if resume.has_status([Status.new.value, 
                                  Status.update.value, 
                                  Status.repeat.value]):
                anketa_schema = AnketaSchema()
                serial = anketa_schema.dump(dict(
                    resume = resume, 
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
                                                    resume.fullname, 
                                                    'check')
                        resume.status = Status.robot.value
                        db.session.add(Check(officer=current_user.fullname, 
                                             path=check_path,
                                             person_id = person_id))
                        db.session.commit()
                        return db.session.query(Person).\
                            filter_by(id=person_id).one_or_none()    
                    return abort(404)
                except requests.exceptions.RequestException as e:
                    print(e)
            return abort(404)

        else:
            return db.session.query(Person).filter_by(id=person_id).one_or_none()    
        
    @roles_required(Roles.user.name)
    @bp.input(PersonSchema)
    def post(self, action, json_data):
        location_id = db.session.query(User.region_id).\
            filter_by(username=current_user.username).scalar()
        person_id, result = add_resume(json_data, location_id, action)
        return {'person_id': person_id}
    
    @roles_required(Roles.user.name)
    @bp.input(PersonSchema)
    def patch(self, person_id, json_data):
        db.session.add(Person(**json_data | {'person_id': person_id}))
        users = db.session.query(User).filter_by(region_id=json_data['region_id']).all()
        for user in users:
            db.session.add(Report(report=f'Делегирована анкета ID #{id} \
                                  от {current_user.username}', user_id=user.id))
        db.session.commit()
        return ''
        
    @roles_required(Roles.user.name)
    def delete(self, person_id):
        person = db.session.query(Person).get(person_id)
        try:
            shutil.rmtree(person.path)
        except Exception as e:
            print(e)
        db.session.delete(person)
        db.session.commit()
        return ''
    
resume_view = ResumeView.as_view('resume')
bp.add_url_rule('/resume/<action>', view_func=resume_view, methods=['POST'])
bp.add_url_rule('/resume/<int:person_id>', view_func=resume_view, methods=['DELETE','PATCH'])
bp.add_url_rule('/resume/<action>/<int:person_id>', view_func=resume_view, methods=['GET'])


class StaffView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(StaffsSchema)
    def get(self, person_id):
        return db.session.query(Staff).filter_by(person_id=person_id).\
            order_by(Staff.id.asc()).all()

    @bp.input(StaffSchema)
    @roles_required(Roles.user.value)
    def post(self, id, json_data):
        db.session.add(Staff(**json_data | {'person_id': id}))
        return ''
        
    @bp.input(StaffSchema)
    @roles_required(Roles.user.value)
    def patch(self, id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Staff).get(id), k, v)
        db.session.commit()
        return ''
   
    @roles_required(Roles.user.name)
    def delete(self, person_id):
        db.session.delete(db.session.query(Staff).get(person_id))
        db.session.commit()
        return ''
    
staff_view = StaffView.as_view('staff')
bp.add_url_rule('/staff', view_func=staff_view, methods=['POST', 'PATCH'])
bp.add_url_rule('/staff/<int:user_id>', view_func=staff_view, methods=['GET', 'DELETE'])


class DocumentView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(DocumentsSchema)
    def get(self, person_id):
        return db.session.query(Document).filter_by(person_id=person_id).\
            order_by(Document.id.asc()).all()
    
    @bp.input(DocumentSchema)
    @roles_required(Roles.user.value)
    def post(self, id, json_data):
        db.session.add(Document(**json_data | {'person_id': id}))
        return ''
        
    @bp.input(DocumentSchema)
    @roles_required(Roles.user.value)
    def patch(self, id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Document).get(id), k, v)
        db.session.commit()
        return ''
   
    @roles_required(Roles.user.name)
    def delete(self, person_id):
        db.session.delete(db.session.query(Document).get(person_id))
        db.session.commit()
        return ''
    
document_view = DocumentView.as_view('document')
bp.add_url_rule('/document', view_func=document_view, methods=['POST', 'PATCH'])
bp.add_url_rule('/document/<int:user_id>', view_func=document_view, methods=['GET','DELETE'])


class AddressView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(AddressesSchema)
    def get(self, person_id):
        return db.session.query(Address).filter_by(person_id=person_id).\
            order_by(Address.id.asc()).all()
    
    @bp.input(AddressSchema)
    @roles_required(Roles.user.value)
    def post(self, id, json_data):
        db.session.add(Address(**json_data | {'person_id': id}))
        return ''
        
    @bp.input(AddressSchema)
    @roles_required(Roles.user.value)
    def patch(self, id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Address).get(id), k, v)
        db.session.commit()
        return ''
   
    @roles_required(Roles.user.name)
    def delete(self, person_id):
        db.session.delete(db.session.query(Address).get(person_id))
        db.session.commit()
        return ''
    
address_view = AddressView.as_view('address')
bp.add_url_rule('/address', view_func=address_view, methods=['POST', 'PATCH'])
bp.add_url_rule('/address/<int:user_id>', view_func=address_view, methods=['GET', 'DELETE'])


class ContactView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(ContactsSchema)
    def get(self, person_id):
        return db.session.query(Contact).filter_by(person_id=person_id).\
            order_by(Contact.id.asc()).all()
    
    @bp.input(ContactSchema)
    @roles_required(Roles.user.value)
    def post(self, id, json_data):
        db.session.add(Contact(**json_data | {'person_id': id}))
        return ''
        
    @bp.input(ContactSchema)
    @roles_required(Roles.user.value)
    def patch(self, id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Contact).get(id), k, v)
        db.session.commit()
        return ''
   
    @roles_required(Roles.user.name)
    def delete(self, person_id):
        db.session.delete(db.session.query(Contact).get(person_id))
        db.session.commit()
        return ''
    
contact_view = ContactView.as_view('contact')
bp.add_url_rule('/contact', view_func=contact_view, methods=['POST', 'PATCH'])
bp.add_url_rule('/contact/<int:user_id>', view_func=contact_view, methods=['GET','DELETE'])


class WorkplaceView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(WorkplacesSchema)
    def get(self, person_id):
        return db.session.query(Workplace).filter_by(person_id=person_id).\
            order_by(Workplace.id.asc()).all()
    
    @bp.input(WorkplaceSchema)
    @roles_required(Roles.user.value)
    def post(self, id, json_data):
        db.session.add(Workplace(**json_data | {'person_id': id}))
        return ''
        
    @bp.input(WorkplaceSchema)
    @roles_required(Roles.user.value)
    def patch(self, id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Workplace).get(id), k, v)
        db.session.commit()
        return ''
   
    @roles_required(Roles.user.name)
    def delete(self, person_id):
        db.session.delete(db.session.query(Workplace).get(person_id))
        db.session.commit()
        return ''
    
workplace_view = AddressView.as_view('workplace')
bp.add_url_rule('/workplace', view_func=workplace_view, methods=['POST', 'PATCH'])
bp.add_url_rule('/workplace/<int:user_id>', view_func=workplace_view, methods=['GET','DELETE'])


class RelationView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(RelationsSchema)
    def get(self, person_id):
        return db.session.query(Relation).filter_by(person_id=person_id).\
            order_by(Relation.id.asc()).all()
    
    @bp.input(RelationSchema)
    @roles_required(Roles.user.value)
    def post(self, id, json_data):
        db.session.add(Relation(**json_data | {'person_id': id}))
        db.session.add(Relation(relation = json_data['relation'], 
                                relation_id = id,
                                person_id = json_data['relation_id']))
        return ''
        
    @bp.input(RelationSchema)
    @roles_required(Roles.user.value)
    def patch(self, id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Relation).get(id), k, v)
        db.session.commit()
        return ''
   
    @roles_required(Roles.user.name)
    def delete(self, person_id):
        db.session.delete(db.session.query(Relation).get(person_id))
        db.session.commit()
        return ''
    
relation_view = RelationView.as_view('relation')
bp.add_url_rule('/relation', view_func=workplace_view, methods=['POST', 'PATCH'])
bp.add_url_rule('/relation/<int:user_id>', view_func=workplace_view, methods=['GET','DELETE'])


class CheckView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(ChecksSchema)
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
        return db.session.query(Check).filter_by(person_id=item_id).\
            order_by(Check.id.asc()).all()
    
    @bp.input(CheckSchema)
    @roles_required(Roles.user.value)
    def post(self, action, item_id, json_data):
        json_data['pfo'] = bool(json_data.pop('pfo')) if 'pfo' in json_data else False
        if action == 'create':
            person = db.session.query(Person).get(item_id)        
            db.session.add(Check(**json_data | {'person_id': item_id, 
                                                'officer': current_user.fullname}))
        else:
            check = db.session.query(Check).get(item_id)
            person = db.session.query(Person).get(check.item_id)
            for k, v in json_data.items():
                setattr(check, k, v)
        db.session.commit()    

        if json_data['conclusion'] == (Status.save.value).upper():
            person.status = Status.save.value
            db.session.commit()
            return {'table': 'check', 
                    'action': action, 
                    'id': item_id, 
                    'message': Status.save.name}
        
        elif json_data['conclusion'] == (Status.cancel.name).upper():
            person.status = Status.result.value
            db.session.commit()
            return {'table': 'check', 
                    'action': action, 
                    'id': item_id, 
                    'message': Status.cancel.name}
        
        else:
            person.status = Status.poligraf.value if json_data['pfo'] \
                else Status.result.value
            db.session.commit()
        
        return {'table': 'check', 
                'action': action, 
                'id': item_id, 
                'message': Status.poligraf.name if json_data['pfo'] \
                    else Status.result.name}
   
    @roles_required(Roles.user.name)
    def delete(self, item_id):
        check = db.session.query(Check).get(item_id)
        db.session.delete(check)
        try:
            shutil.rmtree(check.path)
        except Exception as e:
            print(e)
        person = db.session.query(Person).get(db.session.query(Check.person_id).\
                                              filter_by(id=item_id).scalar())
        person.status = Status.update.value
        db.session.commit()
        return ''
    
check_view = CheckView.as_view('check')
bp.add_url_rule('/checks', view_func=workplace_view, methods=['POST', 'PATCH'])
bp.add_url_rule('/checks/<action>/<int:item_id>', view_func=workplace_view, methods=['GET','DELETE'])


class RegistryView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(RegistriesSchema)
    def get(self, person_id):
        return db.session.query(Registry).filter_by(person_id=person_id).\
            order_by(Registry.id.asc()).all()
    
    @bp.input(RegistrySchema)
    @roles_required(Roles.superuser.value)
    def post(self, id, json_data):
        check_id = db.session.query(Check.id).filter_by(person_id=id).\
            order_by(Check.id.desc()).scalar()
        reg = {'supervisor': current_user.fullname} | json_data
        person = db.session.query(Person).get(id)

        if person.request_id or person.request_id != 'NULL':  
            try:
                response = requests.post(url='https://httpbin.org/post', 
                                        json=json.dumps({"id": person.request_id}
                                                        | reg), timeout=5)
                response.raise_for_status()
                if response.status_code == 200:
                    db.session.add(Registry(**reg | {'check_id': check_id}))
                    person.status = Status.cancel.value \
                        if reg['decision'] == Status.cancel.value else Status.finish.value
                    db.session.commit()
                    return {'message': Status.finish.name}
                else:
                    return {'message': response.text}
            except Exception as e:
                return {"message": e}
        db.session.add(Registry(**reg | {'check_id': check_id}))
        person.status = Status.cancel.value \
            if reg['decision'] == Status.cancel.value else Status.finish.value
        db.session.commit()
        return {'message': Status.finish.name}

registry_view = RegistryView.as_view('registry')
bp.add_url_rule('/registry', view_func=workplace_view, methods=['POST', 'PATCH'])
bp.add_url_rule('/registry/<int:user_id>', view_func=workplace_view, methods=['GET','DELETE'])


class InvestigationView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(InvestigationsSchema)
    def get(self, person_id):
        return db.session.query(Investigation).filter_by(person_id=person_id).\
            order_by(Investigation.id.asc()).all()
    
    @bp.input(InvestigationSchema)
    @roles_required(Roles.user.value)
    def post(self, id, json_data):
        db.session.add(Investigation(**json_data | {'person_id': id, 
                                                    'officer': current_user.fullname}))
        return ''
        
    @bp.input(InvestigationSchema)
    @roles_required(Roles.user.value)
    def patch(self, id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Investigation).get(id), k, v)
        db.session.commit()
        return ''
   
    @roles_required(Roles.user.name)
    def delete(self, person_id):
        invs = db.session.query(Investigation).get(person_id)
        db.session.delete(invs)
        try:
            shutil.rmtree(invs.path)
        except Exception as e:
            print(e)
        db.session.commit()
        return ''
    
investigation_view = InvestigationView.as_view('investigation')
bp.add_url_rule('/investigation', view_func=investigation_view, methods=['POST','PATCH'])
bp.add_url_rule('/investigation/<int:user_id>', view_func=investigation_view, methods=['GET','DELETE'])


class PoligrafView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    db.session.commit()
    @bp.output(PoligrafsSchema)
    def get(self, person_id):
        return db.session.query(Poligraf).filter_by(person_id=person_id).\
            order_by(Poligraf.id.asc()).all()
    
    @bp.input(PoligrafSchema)
    @roles_required(Roles.user.value)
    def post(self, id, json_data):
        person = db.session.query(Person).get(id)
        if person.has_status(Status.poligraf.value):
            person.status = Status.result.value
        db.session.add(Poligraf(**json_data | {'person_id': id, 
                                               'officer': current_user.fullname}))
        return ''
        
    @bp.input(PoligrafSchema)
    @roles_required(Roles.user.value)
    def patch(self, id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Poligraf).get(id), k, v)
        db.session.commit()
        return ''
   
    @roles_required(Roles.user.name)
    def delete(self, person_id):
        db.session.delete(db.session.query(Poligraf).get(person_id))
        db.session.commit()
        return ''
        
pfo_view = PoligrafView.as_view('relation')
bp.add_url_rule('/poligraf', view_func=pfo_view, methods=['POST', 'PATCH'])
bp.add_url_rule('/poligraf/<int:user_id>', view_func=pfo_view, methods=['GET','DELETE'])


class InquiryView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]
    
    @bp.output(InquiriesSchema)
    def get(self, person_id):
        return db.session.query(Inquiry).filter_by(person_id=person_id).\
            order_by(Inquiry.id.asc()).all()
    
    @bp.input(InquirySchema)
    @roles_required(Roles.user.value)
    def post(self, id, json_data):
        db.session.add(Inquiry(**json_data | {'person_id': id, 
                                              'officer': current_user.fullname}))
        return ''
        
    @bp.input(InquirySchema)
    @roles_required(Roles.user.value)
    def patch(self, id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Inquiry).get(id), k, v)
        db.session.commit()
        return ''
   
    @roles_required(Roles.user.name)
    def delete(self, person_id):
        db.session.delete(db.session.query(Inquiry).get(person_id))
        db.session.commit()
        return ''
    
inquiry_view = InquiryView.as_view('inquiry')
bp.add_url_rule('/inquiry', view_func=workplace_view, methods=['POST', 'PATCH'])
bp.add_url_rule('/inquiry/<int:user_id>', view_func=workplace_view, methods=['GET','DELETE'])


class FileView(MethodView):

    @group_required(Groups.staffsec.name)
    @roles_required(Roles.user.name)
    @bp.doc(hide=True)
    def post(self, action, item_id=0):
        if request.files['file'].filename == '':
            return {'result': False, 'item_id': item_id}
        
        if action == 'anketa':
            file = request.files['file']
            
            filename = secure_filename(file.filename)
            temp_path = os.path.join(current_app.config["BASE_PATH"], 
                                     f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}-{filename}')
            file.save(temp_path)
            
            excel = ExcelFile(temp_path)
            location_id = db.session.query(User.region_id).\
                filter_by(username=current_user.username).scalar()

            person_id, result = add_resume(excel.resume, location_id, 'create')
            resume_data(person_id, excel.passport, excel.addresses, 
                        excel.contacts, excel.workplaces, excel.staff)
            excel.close()

            person = Person.query.get(person_id)
            if person and person.path:
                if not os.path.isdir(person.path):
                    os.mkdir(os.path.join(person.path))
                new_path = person.path
            else:
                new_path = os.path.join(current_app.config["BASE_PATH"], 
                                        f'{person_id}-{person["fullname"]}')
                if not os.path.isdir(new_path):
                    os.mkdir(new_path)
                person.path = new_path
                db.session.commit()

            action_folder = os.path.join(new_path, action)
            if not os.path.isdir(action_folder):
                os.mkdir(action_folder)

            save_path = os.path.join(action_folder, filename)
            if not os.path.isfile(save_path):
                shutil.move(temp_path, save_path)
            return {'result': bool(result), 'person_id': person_id}

        else:
            model_mapping = {
                'check': Check,
                'investigation': Investigation,
                'poligraf': Poligraf,
                'inquiry': Inquiry
            }
            files = request.files.getlist('file')
            model = model_mapping.get(action)
            item = db.session.query(model).filter_by(id=item_id).scalar()
            folder = item.path
            if not folder:
                person  = Person.query.get(item.person_id)
                folder = create_folders(person.id, person.fullname, action)
                item.path = folder
                db.session.commit()
            for file in files:
                filename = secure_filename(file.filename)
                for file in files:
                    file.save(os.path.join(folder, filename))
            
            return {'result': bool(result), 'person_id': person_id}

bp.add_url_rule('/file/<action>/<int:item_id>', view_func=FileView.as_view('file'))


class InfoView(MethodView):

    @group_required(Groups.staffsec.name)
    @roles_required(Roles.superuser.name, Roles.user.name)
    @bp.doc(hide=True)
    @jwt_required()
    def post(self):
        response = request.get_json()
        candidates = db.session.query(Registry.decision, func.count(Registry.id)).\
            join(Check, Check.id == Registry.check_id). \
            join(Person, Person.id == Check.person_id).\
            group_by(Registry.decision).\
            filter(Registry.deadline.between(response['start'], response['end']), 
                Person.region_id == int(response['region'])).all()

        pfo = db.session.query(Poligraf.theme, func.count(Poligraf.id)).\
            group_by(Poligraf.theme).filter(Poligraf.deadline.between(response['start'], 
                                                                      response['end'])).all()
        
        return {"candidates": dict(map(lambda x: (x[1], x[0]), candidates)),
            "poligraf": dict(map(lambda x: (x[1], x[0]), pfo))}

bp.add_url_rule('/information', view_func=InfoView.as_view('information'))