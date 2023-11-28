import os
import requests
import shutil
from datetime import datetime

from apiflask import abort, EmptySchema
from flask import request, current_app, send_file
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import and_, extract, func
from werkzeug.utils import secure_filename
from PIL import Image

from . import bp
from .. import db
from .login import r_g
from ..utils.jsonparser import JsonFile
from ..models.model import  User, Person, Staff, Document, Address, Contact, \
    Workplace, Check, Poligraf, Investigation, Inquiry, Relation, \
    Status, Report, Affilation
from ..models.schema import RelationSchema, StaffSchema, AddressSchema, \
    PersonSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
    InvestigationSchema, PoligrafSchema, AnketaSchemaApi, \
    WorkplaceSchema, AffilationSchema, CheckSchemaApi
from ..models.classes import Category, Reports, Roles, Groups, Status


class IndexView(MethodView):
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]

    def __init__(self) -> None:
        self.pagination = 16
        self.location_id = db.session.query(User.region_id). \
            filter_by(username=current_user.username).scalar()
        self.schema = PersonSchema()

    def post(self, flag, page):
        json_data = request.get_json()

        query = db.session.query(Person).order_by(Person.id.desc())
        
        match flag:
            case 'main':
                if self.location_id != 1:
                    query = query.filter_by(region_id=self.location_id)
            case 'new':
                query = query.filter(Person.status.in_([Status.new.value,
                                                        Status.update.value,
                                                        Status.repeat.value]),
                                    Person.region_id == self.location_id,
                                    Person.category == Category.candidate.name)
            case 'officer':
                query = query.filter(Person.status.notin_([Status.finish.value,
                                                            Status.result.value,
                                                            Status.cancel.value])) \
                            .join(Check, isouter=True) \
                            .filter_by(officer=current_user.fullname)
            case 'search':
                if json_data['search']:
                    query = Person.query.search('%{}%'.format(json_data['search'])) 
                    if self.location_id != 1:
                        query = query.filter(Person.region_id == self.location_id)
            
        result = query.paginate(page=page,
                            per_page=self.pagination,
                            error_out=False)
        
        has_next, has_prev = bool(result.has_next), bool(result.has_prev)
        
        return [self.schema.dump(result, many=True),
                {'has_next': has_next, "has_prev": has_prev}]

bp.add_url_rule('/index/<flag>/<int:page>',
                view_func=IndexView.as_view('index'))


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
                anketa_schema = AnketaSchemaApi()
                serial = anketa_schema.dump(dict(
                    resume=person,
                    document=db.session.query(Document). \
                        filter_by(person_id=person_id). \
                        order_by(Document.id.desc()).first(),
                    address=db.session.query(Address). \
                        filter(Address.person_id == person_id,
                               Address.view.ilike("%регистрац%")). \
                        order_by(Address.id.desc()).first()))
                try:
                    response = requests.post(url='https://httpbin.org/post',
                                             json=serial,
                                             timeout=5)
                    response.raise_for_status()
                    if response.status_code == 200:
                        person.status = Status.robot.value
                        db.session.add(Check(officer=current_user.fullname,
                                             person_id=person_id))
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
        location_id = db.session.query(User.region_id). \
            filter_by(username=current_user.username).scalar()
        person_id = self.add_resume(json_data, location_id, action)
        return {'message': person_id}

    @r_g.roles_required(Roles.user.name)
    @bp.input(PersonSchema)
    def patch(self, action, person_id, json_data):
        person = db.session.query(Person).get(person_id)
        person.region_id = json_data['region_id']
        users = db.session.query(User). \
            filter_by(region_id=json_data['region_id']).all()
        if len(users):
            for user in users:
                db.session.add(Report(
                    category=Reports.high.value,
                    report=f'Делегирована анкета #{person_id} \
                                  от {current_user.fullname}', user_id=user.id))
        db.session.commit()
        return '', 201

    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, person_id):
        person = db.session.query(Person).get(person_id)
        try:
            shutil.rmtree(os.path.join(current_app.config['BASE_PATH'], person.path))
        except Exception as e:
            print(e)
        db.session.delete(person)
        db.session.commit()
        return ''

    def add_resume(self, resume: dict, location_id, action):
        """
        Adds a resume to the database.
        """
        result = db.session.query(Person).\
            filter(Person.fullname.ilike(resume['fullname']),
                Person.birthday==resume['birthday']).one_or_none()
        if result:
            if action == "create" or action == 'api':
                resume.update({'status': Status.repeat.value, 'region_id': location_id})
            else:
                resume.update({'status': Status.update.value, 'region_id': location_id})
            for k, v in resume.items():
                setattr(result, k, v)
            person_id = result.id
            
            if result.path and not os.path.isdir(os.path.join(current_app.config["BASE_PATH"], 
                                                            result.path)):
                os.mkdir(result.path)
            elif not result.path:
                new_path = os.path.join(current_app.config["BASE_PATH"], 
                                        resume['fullname'][0].upper(),
                                        f'{person_id}-{resume["fullname"]}')
                if not os.path.isdir(new_path):
                    os.mkdir(new_path)
                result.path = os.path.join(resume['fullname'][0].upper(), 
                                        f'{person_id}-{resume["fullname"]}')
        else:
            person = Person(**resume | {'region_id': location_id})
            db.session.add(person)
            db.session.flush()
            person_id = person.id
            
            path = os.path.join(current_app.config["BASE_PATH"], 
                                resume['fullname'][0].upper(),
                                f'{person_id}-{resume["fullname"]}')
            if not os.path.isdir(path):
                os.mkdir(path)
            
            person.path = os.path.join(resume['fullname'][0].upper(),
                                    f'{person_id}-{resume["fullname"]}')

        db.session.commit()
        return person_id

resume_view = ResumeView.as_view('resume')
bp.add_url_rule('/resume/<action>',
                view_func=resume_view, methods=['POST'])
bp.add_url_rule('/resume/<action>/<int:person_id>',
                view_func=resume_view, methods=['GET', 'PATCH', 'DELETE'])


class StaffView(MethodView):
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]

    def get(self, action, item_id):
        schema = StaffSchema()
        return schema.dump(db.session.query(Staff). \
                           filter_by(person_id=item_id). \
                           order_by(Staff.id.desc()).all(), many=True)

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
        return schema.dump(db.session.query(Document). \
                           filter_by(person_id=item_id). \
                           order_by(Document.id.desc()).all(), many=True)

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
        return schema.dump(db.session.query(Address). \
                           filter_by(person_id=item_id). \
                           order_by(Address.id.desc()).all(), many=True)

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
        return schema.dump(db.session.query(Contact). \
                           filter_by(person_id=item_id). \
                           order_by(Contact.id.desc()).all(), many=True)

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
        return schema.dump(db.session.query(Workplace). \
                           filter_by(person_id=item_id). \
                           order_by(Workplace.id.desc()).all(), many=True)

    @r_g.roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    def post(self, action, item_id, json_data):
        json_data['now_work'] = bool(json_data.pop('now_work')) \
            if 'now_work' in json_data else False
        db.session.add(Workplace(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201

    @r_g.roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    def patch(self, action, item_id, json_data):
        json_data['now_work'] = bool(json_data.pop('now_work')) \
            if 'now_work' in json_data else False
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
        return schema.dump(db.session.query(Relation). \
                           filter_by(person_id=item_id). \
                           order_by(Relation.id.desc()).all(), many=True)

    @r_g.roles_required(Roles.user.value)
    @bp.input(RelationSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Relation(**json_data | {'person_id': item_id}))
        db.session.add(Relation(relation=json_data['relation'],
                                relation_id=item_id,
                                person_id=json_data['relation_id']))
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


class AffilationView(MethodView):
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]

    def get(self, action, item_id):
        schema = AffilationSchema()
        return schema.dump(db.session.query(Affilation). \
                           filter_by(person_id=item_id). \
                           order_by(Affilation.id.desc()).all(), many=True)

    @r_g.roles_required(Roles.user.value)
    @bp.input(AffilationSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Affilation(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201

    @r_g.roles_required(Roles.user.value)
    @bp.input(AffilationSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Affilation).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Affilation).get(item_id))
        db.session.commit()
        return ''

bp.add_url_rule('/affilation/<action>/<int:item_id>',
                view_func=AffilationView.as_view('affilation'))


class CheckView(MethodView):
    
    @r_g.group_required(Groups.staffsec.name)
    @bp.doc(hide=True)
    def get(self, action, item_id):
        if action == 'add':
            person = db.session.query(Person).get(item_id)
            if person.has_status([Status.new.value,
                                  Status.update.value,
                                  Status.repeat.value]):
                person.status = Status.manual.value
                db.session.add(Check(officer=current_user.fullname,
                                     person_id=item_id))
                db.session.commit()
                return '', 201

        if action == 'self':
            check = db.session.query(Check).get(item_id)
            prev_officer = db.session.query(User).\
                filter_by(fullname=check.officer).one_or_none()
            new_officer = db.session.query(User).\
                filter_by(fullname=current_user.fullname).one_or_none()
            db.session.add(Report(category=Reports.high.value, 
                                  report=f'Aнкета ID #{id} делегирована {current_user.fullname}', user_id=prev_officer.id))
            check.officer = current_user.fullname
            db.session.add(Report(category=Reports.high.value, 
                                  report=f'Aнкета ID #{id} переделегирована {current_user.fullname}', user_id=new_officer.id))
            db.session.commit()
            return '', 201

        schema = CheckSchema()
        return schema.dump(db.session.query(Check). \
                           filter_by(person_id=item_id). \
                           order_by(Check.id.desc()).all(), many=True)

    @r_g.roles_required(Roles.api.name)
    @bp.doc(hide=False)
    @bp.input(CheckSchemaApi)
    def post(json_data):
        candidate = db.session.query(Person).get(json_data['id'])
        del json_data['id']
        latest_check = db.session.query(Check).filter_by(person_id=candidate.id).\
            order_by(Check.id.desc()).first()
        user = db.session.query(User).filter_by(fullname=latest_check.officer).one_or_none()
        
        if candidate.status == Status.robot.value:
            if os.path.isdir(json_data['path']):
                file_view = FileView()
                full_path = os.path.join(current_app.config["BASE_PATH"], latest_check.path)
                check_path = full_path if os.path.isdir(full_path) \
                    else file_view.create_folders(candidate.id, candidate["fullname"], 'check')
                
                try:
                    for item in os.listdir(json_data['path']):
                        if os.path.isfile(os.path.join(json_data['path'], item)):
                            shutil.copyfile(item, check_path)
                        elif os.path.isdir(os.path.join(json_data['path'], item)):
                            shutil.copytree(item, os.path.join(check_path, item))

                except FileNotFoundError as error:
                    db.session.add(Report(report=f'{error}', user_id=user.id))
                
            for k, v in json_data.items():
                setattr(latest_check, k, v)
            db.session.add(Report(report=f'Проверка кандидата \
                                    {candidate.fullname} окончена', user_id=user.id))
            candidate.status = Status.reply.value
            db.session.commit()   

        else:
            db.session.add(Report(report=f'Результат проверки \
                                {candidate.fullname} не может быть записан. \
                                    Материал проверки находится в {json_data["path"]}', 
                                    user_id=user.id))
            db.session.commit()

        return '', 201
    
    @r_g.roles_required(Roles.user.value)
    @bp.input(CheckSchema)
    @bp.doc(hide=True)
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
    @bp.doc(hide=True)
    def delete(self, action, item_id):
        check = db.session.query(Check).get(item_id)
        try:
            shutil.rmtree(os.path.join(current_app.config['BASE_PATH'], check.path))
        except Exception as e:
            print(e)
        person = db.session.query(Person).get(db.session.query(Check.person_id). \
                                              filter_by(id=item_id).one_or_none())
        person.status = Status.update.value
        db.session.delete(check)
        db.session.commit()
        return ''


bp.add_url_rule('/check/<action>/<int:item_id>',
                view_func=CheckView.as_view('check'))


class InvestigationView(MethodView):
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]

    def get(self, action, item_id):
        schema = InvestigationSchema()
        return schema.dump(db.session.query(Investigation). \
                           filter_by(person_id=item_id). \
                           order_by(Investigation.id.desc()).all(), many=True)

    @r_g.roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Investigation(**json_data | {'person_id': item_id,
                                                    'officer': current_user.fullname}))
        db.session.commit()
        return '', 201

    @r_g.roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Investigation).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @r_g.roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        invs = db.session.query(Investigation).get(item_id)
        try:
            shutil.rmtree(os.path.join(current_app.config['BASE_PATH'], invs.path))
        except Exception as e:
            print(e)
        db.session.delete(invs)
        db.session.commit()
        return ''


bp.add_url_rule('/investigation/<action>/<int:item_id>',
                view_func=InvestigationView.as_view('investigation'))


class PoligrafView(MethodView):
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]

    def get(self, action, item_id):
        schema = PoligrafSchema()
        return schema.dump(db.session.query(Poligraf). \
                           filter_by(person_id=item_id). \
                           order_by(Poligraf.id.desc()).all(), many=True)

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
        pfo = db.session.query(Poligraf).get(item_id)
        try:
            shutil.rmtree(os.path.join(current_app.config['BASE_PATH'], pfo.path))
        except Exception as e:
            print(e)
        db.session.delete(pfo)
        db.session.commit()
        return ''


bp.add_url_rule('/poligraf/<action>/<int:item_id>',
                view_func=PoligrafView.as_view('poligraf'))


class InquiryView(MethodView):
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]

    def get(self, action, item_id):
        schema = InquirySchema()
        return schema.dump(db.session.query(Inquiry). \
                           filter_by(person_id=item_id). \
                           order_by(Inquiry.id.desc()).all(), many=True)

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


class InfoView(MethodView):
    decorators = [r_g.group_required(Groups.staffsec.name), bp.doc(hide=True)]

    def post(self):
        response = request.get_json()

        candidates = db.session.query(
            extract('month', Check.deadline).label('month'),
            Check.conclusion,
            func.count(Check.id)
        ). \
            join(Person, Person.id == Check.person_id). \
            group_by(Check.conclusion, extract('month', Check.deadline)). \
            filter(and_(Check.deadline.between(response['start'],
                                                  response['end']), 
                        Person.region_id == int(response['region']))).all()

        pfo = db.session.query(Poligraf.theme, func.count(Poligraf.id)). \
            group_by(Poligraf.theme). \
            filter(Poligraf.deadline.between(response['start'],
                                             response['end'])).all()

        return {"candidates": [
            {'month': row[0], 'decision': row[1], 'count': row[2]}
            for row in candidates
        ],
            "poligraf": dict(pfo)
        }


bp.add_url_rule('/information', view_func=InfoView.as_view('information'))


class FileView(MethodView):

    decorators = [r_g.group_required(Groups.staffsec.name),
                  r_g.roles_required(Roles.user.name),
                  bp.doc(hide=True)]

    def get(self, action, item_id):
        """
        Retrieves a file from the server and sends it as a response.

        Parameters:
            action (str): The action to perform.
            item_id (int): The ID of the item to retrieve.

        Returns:
            FileResponse: The file response containing the requested file, if it exists.
        """
        person = db.session.query(Person).get(item_id)
        file_path = os.path.join(current_app.config['BASE_PATH'], 
                                 person.path, 'images', 'image.jpg')
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        return abort(404)

    def post(self, action, item_id=0):

        if not request.files['file'].filename:
            return {'result': False, 'item_id': item_id}

        resume_view = ResumeView()
        if action == 'anketa':
            location_id = db.session.query(User.region_id). \
                filter_by(username=current_user.username).scalar()
                       
            file = request.files['file']

            filename = secure_filename(file.filename)
            temp_path = os.path.join(current_app.config["BASE_PATH"],
                                     f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}\
                                        -{filename}')
            file.save(temp_path)
            
            anketa  = JsonFile(temp_path)
            person_id = resume_view.add_resume(anketa.resume, location_id, 'create')
            models = [Staff, Document, Address, Contact, Workplace, Affilation]
            for idx, items in enumerate([anketa.staff, anketa.passport, 
                                           anketa.addresses, anketa.contacts, 
                                           anketa.workplaces, anketa.affilation]):
                for item in items:
                    if item:
                        db.session.add(models[idx](**item | {'person_id': person_id}))
            db.session.commit()

            person = db.session.query(Person).get(person_id)
            if person.path:
                full_path = os.path.join(current_app.config["BASE_PATH"], person.path)
                if not os.path.isdir(full_path):
                    os.mkdir(full_path)
            else:
                full_path = os.path.join(current_app.config["BASE_PATH"],
                                        person.fullname[0].upper(),
                                        f'{person_id}-{person.fullname}')
                
                if not os.path.isdir(full_path):
                    os.mkdir(full_path)
                person.path = os.path.join(person.fullname[0].upper(), 
                                           f'{person_id}-{person.fullname}')
                db.session.commit()

            action_folder = self.create_folders(person_id, person.fullname, action)

            save_path = os.path.join(current_app.config["BASE_PATH"], action_folder, filename)
            if not os.path.isfile(save_path):
                shutil.move(temp_path, save_path)
            return {'message': person_id}

        else:
            model_mapping = {
                'check': Check,
                'investigation': Investigation,
                'poligraf': Poligraf,
                'image': Person
            }
            files = request.files.getlist('file')
            model = model_mapping.get(action)
            item = db.session.query(model).filter_by(id=item_id).scalar()
            person = db.session.query(Person).get(item.person_id)
            folder = self.create_folders(person.id, person.fullname, action)
            if action == 'image':
                im = Image.open(files[0])
                rgb_im = im.convert('RGB')
                images = os.path.join(current_app.config["BASE_PATH"], folder, 'images')
                if not os.path.isdir(images):
                    os.mkdir(images)
                image_path = os.path.join(images, 'image.jpg')
                if os.path.isfile(image_path):
                    os.remove(image_path)
                rgb_im.save(image_path)
            else:
                for file in files:
                    filename = secure_filename(file.filename)
                    for file in files:
                        file.save(os.path.join(current_app.config["BASE_PATH"], folder,
                            f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}-{filename}'))
            return {'message': item_id}   

    def create_folders(self, person_id, fullname, folder_name):
        """
        Check if a folder exists for a given person and create it if it does not exist.
        """
        url = os.path.join(current_app.config["BASE_PATH"], 
                        fullname[0].upper(), 
                        f'{person_id}-{fullname}')
        if not os.path.isdir(url):
            os.mkdir(url)
        folder = os.path.join(url, folder_name)
        if not os.path.isdir(folder):
            os.mkdir(folder)
        if folder_name == 'image':
            return folder
        subfolder = os.path.join(folder, datetime.now().strftime("%Y-%m-%d"))
        if not os.path.isdir(subfolder):
            os.mkdir(subfolder)
        return os.path.join(fullname[0].upper(), 
                            f'{person_id}-{fullname}', 
                            folder, subfolder)
                            
bp.add_url_rule('/file/<action>/<int:item_id>',
                view_func=FileView.as_view('file'))