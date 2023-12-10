import asyncio
import os
import shutil
from datetime import datetime
from apiflask import EmptySchema

from flask import request, current_app, send_file, abort
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select, and_, extract, func
from werkzeug.utils import secure_filename
from PIL import Image
import requests

from . import bp
from .. import db
from .login import roles_required, group_required
from ..utils.jsonparser import JsonFile
from ..models.model import  Category, Conclusion, User, Person, Staff, Document, Address, Contact, \
    Workplace, Check, Poligraf, Investigation, Inquiry, Relation, \
    Status, Message, Affilation, Risk, Robot
from ..models.schema import RelationSchema, StaffSchema, AddressSchema, \
    PersonSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
    InvestigationSchema, PoligrafSchema, AnketaSchemaApi, \
    WorkplaceSchema, AffilationSchema, CheckSchemaApi, RiskSchema, RobotSchema
from ..models.classes import Categories, Conclusions, Roles, Groups, Statuses


class IndexView(MethodView):

    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]

    def post(self, flag, page):
        json_data = request.get_json()
        query = db.session.query(Person).order_by(Person.id.desc())
        
        match flag:
            case 'new':
                query = query.filter(
                    Person.status_id.in_([Statuses.new.value,
                                          Statuses.update.value,
                                          Statuses.repeat.value]),
                    Person.category_id == Categories.candidate.value)
            case 'officer':
                query = (query
                         .filter(Person.has_status(Statuses.finish.value) or 
                                 Person.has_status(Statuses.cancel.value))
                         .join(Check, isouter=True) \
                         .filter_by(officer=current_user.fullname))
            case 'search':
                if json_data['search']:
                    query = Person.query.search('%{}%'.format(json_data['search'])) 
            
        result = query.paginate(page=page, per_page=16, error_out=False)       
        return [
            PersonSchema().dump(result, many=True),
            {'has_next': bool(result.has_next), "has_prev": bool(result.has_prev)}
            ]
    
bp.add_url_rule('/index/<flag>/<int:page>',
                view_func=IndexView.as_view('index'))


class PersonView(MethodView):

    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]

    async def get(self, person_id):
        views = [
            ResumeView(), StaffView(), DocumentView(), ContactView(),
            AddressView(), WorkplaceView(), AffilationView(), RelationView(),
            CheckView(), PoligrafView(), InvestigationView(), InquiryView()
        ]
        items = ['resume', 'staffs', 'documents', 'contacts', 'addresses', 'works',
                 'affilations', 'relations', 'checks', 'poligafs', 'investigations', 'inquiries']
        results = []
        results.extend(*[{item: view.get('view', person_id)} for view, item in zip(views, items)])
    
        return {'person': results}
    
bp.add_url_rule('/person/<int:person_id>', view_func=PersonView.as_view('person'))


class ResumeView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]

    @bp.output(PersonSchema)
    def get(self, action, person_id):
        person = db.session.query(Person).get(person_id)
        
        if action == 'status':
            person.status_id = (db.session
                                .query(Status)
                                .filter_by(status=Statuses.update.value)
                                .one_or_none().id)
            db.session.commit()
            return db.session.query(Person).get(person_id)
        
        elif action == 'send':
            if (person.has_status(Statuses.new.value) or
                person.has_status(Statuses.update.value) or
                person.has_status([Statuses.repeat.value])):

                docum = (db.session
                            .query(Document)
                            .filter_by(person_id=person_id)
                            .order_by(Document.id.desc())
                            .one_or_none())
                addr = (db.session
                           .query(Address)
                           .filter(Address.person_id == person_id,
                                  Address.view.ilike("%регистрац%"))
                           .order_by(Address.id.desc())
                           .one_or_none())
                serial = AnketaSchemaApi().dump(
                    dict(
                        resume=person,
                        document=docum,
                        address=addr)
                        )
                try:
                    response = requests.post(
                        url='https://httpbin.org/post',
                        json=serial,
                        timeout=5
                        )
                    response.raise_for_status()
                    if response.status_code == 200:
                        person.status_id = (db.session
                                            .query(Status)
                                            .filter_by(status=Statuses.robot.value)
                                            .one_or_none().id)
                        db.session.add(
                            Check(officer=current_user.fullname,
                                  person_id=person_id)
                                  )
                        db.session.commit()
                        return db.session.query(Person).get(person_id)
                    
                    return abort(response.status_code)
                except requests.exceptions.RequestException as e:
                    print(e)
            return abort(404)
        return person
    
    @roles_required(Roles.user.name, Roles.api.name)
    @bp.input(PersonSchema)
    def post(self, action, json_data):
        person_id = self.add_resume(json_data, action)
        return {'message': person_id}

    @roles_required(Roles.user.name)
    def delete(self, action, person_id):
        person = db.session.get(Person, person_id)
        try:
            shutil.rmtree(os.path.join(current_app.config['BASE_PATH'], person.path))
        except Exception as e:
            print(e)
        db.session.delete(person)
        db.session.commit()
        return ''

    async def add_resume(self, resume: dict, action):
        """
        Adds a resume to the database.
        """
        person = (db.session
                  .query(Person)
                  .filter(Person.fullname.ilike(resume['fullname']),
                          Person.birthday==resume['birthday'])
                  .one_or_none())
        if person:
            statuses = db.session.query(Status)
            status_id = (statuses
                         .filter_by(status=Statuses.new.value).first().id 
                            if action in ["create", "api"] else 
                        statuses
                         .filter_by(status=Statuses.update.value).first().id)
            person.update(**resume)
            person.status_id = status_id
            person_id = person.id
        else:
            person = Person(**resume)
            await db.session.add(person)
            await db.session.flush()
            person_id = person.id

        person.path = self.make_folder(resume['fullname'], person_id)
        db.session.commit()
        return person_id
    
    def make_folder(self, fullname, person_id):
        """
        Check if a folder exists for a given person and create it if it does not exist.
        """
        person_path = os.path.join(fullname[0].upper(), person_id, fullname)
        url = os.path.join(current_app.config["BASE_PATH"], person_path)
        if not os.path.isdir(url):
            os.mkdir(url)
        return person_path

resume_view = ResumeView.as_view('resume')
bp.add_url_rule('/resume/<action>',
                view_func=resume_view, methods=['POST'])
bp.add_url_rule('/resume/<action>/<int:person_id>',
                view_func=resume_view, methods=['GET', 'DELETE'])

class StaffView(MethodView):

    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]
    
    def get(self, action, item_id):
        return StaffSchema().dump(db.session
                           .query(Staff)
                           .filter_by(person_id=item_id)
                           .order_by(Staff.id.desc())
                           .all(), many=True)
    
    @bp.input(StaffSchema)
    @roles_required(Roles.user.value)
    def post(self, action, item_id, json_data):
        db.session.add(Staff(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201
    
    @bp.input(StaffSchema)
    @roles_required(Roles.user.value)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Staff).get(item_id), k, v)
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Staff).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/staff/<action>/<int:item_id>',
                view_func=StaffView.as_view('staff'))


class DocumentView(MethodView):

    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]
    
    def get(self, action, item_id):
        return DocumentSchema().dump(db.session
                                     .query(Document)
                                     .filter_by(person_id=item_id)
                                     .order_by(Document.id.desc())
                                     .all(), many=True)
    
    @roles_required(Roles.user.value)
    @bp.input(DocumentSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Document(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.value)
    @bp.input(DocumentSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Document).get(item_id), k, v)
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Document).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/document/<action>/<int:item_id>',
                view_func=DocumentView.as_view('document'))


class AddressView(MethodView):

    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]
    
    def get(self, action, item_id):
        return AddressSchema().dump(db.session
                                    .query(Address)
                                    .filter_by(person_id=item_id)
                                    .order_by(Address.id.desc())
                                    .all(), many=True)
    
    @roles_required(Roles.user.value)
    @bp.input(AddressSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Address(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.value)
    @bp.input(AddressSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Address).get(item_id), k, v)
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Address).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/address/<action>/<int:item_id>',
                view_func=AddressView.as_view('address'))


class ContactView(MethodView):

    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]
    
    def get(self, action, item_id):
        return ContactSchema().dump(db.session
                                    .query(Contact)
                                    .filter_by(person_id=item_id)
                                    .order_by(Contact.id.desc())
                                    .all(), many=True)
    
    @roles_required(Roles.user.value)
    @bp.input(ContactSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Contact(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.value)
    @bp.input(ContactSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Contact).get(item_id), k, v)
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Contact).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/contact/<action>/<int:item_id>',
                view_func=ContactView.as_view('contact'))


class WorkplaceView(MethodView):

    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]
    
    def get(self, action, item_id):
        return WorkplaceSchema().dump(db.session
                                      .query(Workplace)
                                      .filter_by(person_id=item_id)
                                      .order_by(Workplace.id.desc())
                                      .all(), many=True)
    
    @roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    def post(self, action, item_id, json_data):
        json_data['now_work'] = bool(json_data.pop('now_work')) \
            if 'now_work' in json_data else False
        db.session.add(Workplace(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    def patch(self, action, item_id, json_data):
        json_data['now_work'] = bool(json_data.pop('now_work')) \
            if 'now_work' in json_data else False
        for k, v in json_data.items():
            setattr(db.session.query(Workplace).get(item_id), k, v)
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Workplace).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/workplace/<action>/<int:item_id>',
                view_func=WorkplaceView.as_view('workplace'))


class RelationView(MethodView):
    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]
    
    def get(self, action, item_id):
        return RelationSchema().dump(db.session
                                     .query(Relation)
                                     .filter_by(person_id=item_id)
                                     .order_by(Relation.id.desc())
                                     .all(), many=True)
    
    @roles_required(Roles.user.value)
    @bp.input(RelationSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Relation(**json_data | {'person_id': item_id}))
        db.session.add(Relation(relation=json_data['relation'],
                                relation_id=item_id,
                                person_id=json_data['relation_id']))
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.value)
    @bp.input(RelationSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Relation).get(item_id), k, v)
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Relation).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/relation/<action>/<int:item_id>',
                view_func=RelationView.as_view('relation'))


class AffilationView(MethodView):

    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]
    
    def get(self, action, item_id):
        schema = AffilationSchema()
        return schema.dump(db.session
                           .query(Affilation)
                           .filter_by(person_id=item_id)
                           .order_by(Affilation.id.desc())
                           .all(), many=True)
    
    @roles_required(Roles.user.value)
    @bp.input(AffilationSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Affilation(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.value)
    @bp.input(AffilationSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Affilation).get(item_id), k, v)
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Affilation).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/affilation/<action>/<int:item_id>',
                view_func=AffilationView.as_view('affilation'))


class CheckView(MethodView):

    def get(self, action, item_id):
        if action == 'add':
            person = db.session.query(Person).get(item_id)
            if (person.has_status(Statuses.new.value) or
                person.has_status(Statuses.update.value) or 
                person.has_status(Statuses.repeat.value)):
                person.status_id = (db.session
                                    .query(Status)
                                    .filter_by(status=Statuses.manual.value)
                                    .one_or_none().id)
                db.session.add(Check(
                    officer=current_user.fullname, person_id=item_id)
                    )
                db.session.commit()
                return '', 201
            
        if action == 'self':
            check = db.session.query(Check).get(item_id)
            prev_officer = (db.session
                            .query(User)
                            .filter_by(fullname=check.officer)
                            .one_or_none())
            new_officer = (db.session
                           .query(User)
                           .filter_by(fullname=current_user.fullname)
                           .one_or_none())
            db.session.add(Message(message=f'Aнкета ID #{id} делегирована '
                                            f'{current_user.fullname}', 
                                   user_id=prev_officer.id))
            check.officer = current_user.fullname
            db.session.add(Message(message=f'Aнкета ID #{id} переделегирована '
                                            f'{current_user.fullname}', 
                                   user_id=new_officer.id))
            db.session.commit()
            return '', 201
        schema = CheckSchema()
        return schema.dump(db.session.query(Check). \
                           filter_by(person_id=item_id). \
                           order_by(Check.id.desc()).all(), many=True)


    @roles_required(Roles.user.value)
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
        save_id = (db.session
                   .query(Conclusion)
                   .filter_by(status=Conclusions.saved.value)
                   .one_or_none().id)
        if json_data['conclusion_id'] == save_id:
            person.status_id = (db.session
                                .query(Status)
                                .filter(Status.status == Statuses.save.value)
                                .one_or_none().id)
        else:
            pfo_id = (db.session
                  .query(Status)
                  .filter_by(status=Statuses.poligraf.value)
                  .one_or_none().id)
            finish_id = (db.session
                         .query(Status)
                         .filter_by(status=Statuses.finish.value)
                         .one_or_none().id)
            person.status_id = pfo_id if json_data['pfo'] else finish_id
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
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


class RobotView(MethodView):
    """
    The RobotView class is a subclass of the MethodView class from the flask.views module.
    """
    decorators = [group_required(Groups.api.name), 
                  roles_required(Roles.api.name)]

    @bp.doc(hide=False)
    @bp.input(RobotSchema)
    def post(self, json_data):
        candidate = db.session.get(Person, json_data['id'])
        del json_data['id']
        latest_check = db.session.execute(
            select(Check)
            .filter_by(person_id=candidate.id)
            .order_by(Check.id.desc())
            ).first()
        user = db.session.execute(
            select(User)
            .filter_by(fullname=latest_check.officer)
            ).one_or_none()
        if candidate.status_id == db.session.execute(
            select(Status)
            .filter(Status.status == Statuses.robot.value)
            ).first().id:
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
                    db.session.add(Message(report=f'{error}', user_id=user.id))

            for k, v in json_data.items():
                setattr(latest_check, k, v)
            db.session.add(Message(
                report=f'Проверка кандидата {candidate.fullname} окончена', 
                user_id=user.id)
                )
            candidate.status_id = db.session.execute(
                select(Status)
                .filter(Status.status == Statuses.reply.value)
                ).first().id
            db.session.commit()

        else:
            db.session.add(Message(
                report=f'Результат проверки {candidate.fullname} не может быть записан.'
                       f'Материал проверки находится в {json_data["path"]}', 
                user_id=user.id))
            db.session.commit()

        return '', 201

bp.add_url_rule('/robot/<int:item_id>', view_func=RobotView.as_view('robot'))


class InvestigationView(MethodView):

    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]

    def get(self, action, item_id):
        return InvestigationSchema().dump(db.session.execute(
            select(Investigation)
            .filter_by(person_id=item_id)
            .order_by(Investigation.id.desc())
            ).all(), many=True)
    
    @roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    def post(self, action, item_id, json_data):
        db.session.add(Investigation(
            **json_data | {'person_id': item_id, 'officer': current_user.fullname}
            ))
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Investigation).get(item_id), k, v)
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        invs = db.session.query(Investigation).get(item_id)
        db.session.delete(invs)
        db.session.commit()
        return ''
    
bp.add_url_rule('/investigation/<action>/<int:item_id>',
                view_func=InvestigationView.as_view('investigation'))


class PoligrafView(MethodView):

    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]
    
    def get(self, action, item_id):
        return PoligrafSchema().dump(db.session.execute(
            select(Poligraf)
            .filter_by(person_id=item_id)
            .order_by(Poligraf.id.desc())
            ).all(), many=True)
    
    @roles_required(Roles.user.value)
    @bp.input(PoligrafSchema)
    def post(self, action, item_id, json_data):
        person = db.session.query(Person).get(item_id)
        if person.has_status(Statuses.poligraf.value):
            person.status_id = db.session.execute(
                select(Status)
                .filter(Status.status == Statuses.finish.value)
                ).one_or_none().id
        db.session.add(Poligraf(
            **json_data | {'person_id': item_id, 'officer': current_user.fullname}
            ))
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.value)
    @bp.input(PoligrafSchema)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Poligraf).get(item_id), k, v)
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        pfo = db.session.query(Poligraf).get(item_id)
        db.session.delete(pfo)
        db.session.commit()
        return ''
    
bp.add_url_rule('/poligraf/<action>/<int:item_id>',
                view_func=PoligrafView.as_view('poligraf'))


class InquiryView(MethodView):

    decorators = [group_required(Groups.staffsec.name), 
                  bp.doc(hide=True)]
    
    def get(self, action, item_id):
        return InquirySchema().dump(db.session.execute(
            select(Inquiry)
            .filter_by(person_id=item_id)
            .order_by(Inquiry.id.desc())
            ).all(), many=True)
    
    @bp.input(InquirySchema)
    @roles_required(Roles.user.value)
    def post(self, action, item_id, json_data):
        db.session.add(Inquiry(**json_data | {'person_id': item_id,
                                              'officer': current_user.fullname}))
        db.session.commit()
        return '', 201
    
    @bp.input(InquirySchema)
    @roles_required(Roles.user.value)
    def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(db.session.query(Inquiry).get(item_id), k, v)
        db.session.commit()
        return '', 201
    
    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    def delete(self, action, item_id):
        db.session.delete(db.session.query(Inquiry).get(item_id))
        db.session.commit()
        return ''
    
bp.add_url_rule('/inquiry/<action>/<int:item_id>',
                view_func=InquiryView.as_view('inquiry'))

class InfoView(MethodView):
    @group_required(Groups.staffsec.name)
    @bp.doc(hide=True)
    def post(self):
        response = request.get_json()
        candidates = db.session.execute(
            select(Check.conclusion, func.count(Check.id))
            .join(Person)
            .group_by(Check.conclusion)
            .filter(Person.region_id == response['region_id'])
            .filter(Check.deadline.between(response['start'], response['end']))
            ).all()
        return {"candidates": dict(map(lambda x: (x[1], x[0]), candidates))}
    
bp.add_url_rule('/information', view_func=InfoView.as_view('information'))


class FileView(MethodView):

    decorators = [group_required(Groups.staffsec.name),
                  roles_required(Roles.user.name),
                  bp.doc(hide=True)]

    def get(self, action, item_id):
        """
        Retrieves a file from the server and sends it as a response.
        """
        person = db.session.get(Person, item_id)
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
            file = request.files['file']
            filename = secure_filename(file.filename)
            temp_path = os.path.join(current_app.config["BASE_PATH"],
                                    f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}\
                                        -{filename}')
            file.save(temp_path)
            
            anketa  = JsonFile(temp_path)
            person_id = resume_view.add_resume(anketa.resume, 'create')
            models = [Staff, Document, Address, Contact, Workplace, Affilation]
            items_lists = [anketa.staff, anketa.passport, anketa.addresses, 
                            anketa.contacts, anketa.workplaces, anketa.affilation]
            for model, items in zip(models, items_lists):
                for item in items:
                    if item:
                        db.session.add(model(**item | {'person_id': person_id}))

            person = db.session.get(Person, person_id)
            if person.path:
                full_path = os.path.join(current_app.config["BASE_PATH"], person.path)
                if not os.path.isdir(full_path):
                    os.mkdir(full_path)
            else:
                person.path = resume_view.make_folder(person.fullname, person_id)
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
            item = db.session.get(model, item_id)
            person = db.session.get(Person, item.person_id)
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

    async def create_folders(self, person_id, fullname, folder_name):
        """
        Check if a folder exists for a given person and create it if it does not exist.
        """
        resume_view = ResumeView()
        url = os.path.join(current_app.config["BASE_PATH"], 
                           resume_view.make_folder(fullname, person_id))
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