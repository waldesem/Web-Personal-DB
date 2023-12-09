import asyncio
import os
import shutil
from datetime import datetime

from flask import request, current_app, send_file, abort
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import select, and_, extract, func
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.utils import secure_filename
from PIL import Image
import aiohttp

from . import bp
from .login import roles_required, group_required
from ..utils.jsonparser import JsonFile
from ..models.model import  Category, Conclusion, User, Person, Staff, Document, Address, Contact, \
    Workplace, Check, Poligraf, Investigation, Inquiry, Relation, \
    Status, Message, Affilation, engine
from ..models.schema import RelationSchema, StaffSchema, AddressSchema, \
    PersonSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
    InvestigationSchema, PoligrafSchema, AnketaSchemaApi, \
    WorkplaceSchema, AffilationSchema, CheckSchemaApi
from ..models.classes import Categories, Conclusions, Roles, Groups, Statuses
from ..models.paginate import Pagination


class IndexView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def __init__(self) -> None:
        """
        Initializes a new instance of the class.
        """
        self.pagination = 16
        self.schema = PersonSchema()

    async def post(self, flag, page):
        json_data = request.get_json()
        async with AsyncSession(engine) as session:
            async with session.begin():
                categories_query = await session.execute(select(Category))
                categories = {category.category: category.id 
                              for category in categories_query.scalars()}
                statuses_query = await session.execute(select(Status))
                statuses = {status.status: status.id 
                            for status in statuses_query.scalars()}
            match flag:
                case 'new':
                    query = await session.execute(
                        select(Person)
                        .order_by(Person.id.desc())
                        .filter(
                            Person.status_id.in_(
                                [
                                    statuses.get(Statuses.new.value),
                                    statuses.get(Statuses.update.value),
                                    statuses.get(Statuses.repeat.value),
                                ]
                            ),
                            Person.category_id ==  categories.get(Categories.candidate.name)
                            )
                    )
                case 'officer':
                    query = await session.execute(
                        select(Person)
                        .order_by(Person.id.desc())
                        .filter(
                            Person.status_id.notin_(
                                [
                                    statuses.get(Statuses.finish.value),
                                    statuses.get(Statuses.cancel.value)
                                ]
                            )
                        ) 
                        .join(Check, isouter=True) \
                        .filter_by(officer=get_jwt_identity())
                    )
                case 'search':
                    query = await session.execute(
                        select(Person)
                        .filter(
                            Person.fullname.ilike(
                                '%{}%'.format(json_data['search'])
                            )
                        )
                        .order_by(Person.id.desc())
                    )                      
            pagination = Pagination(query.scalars(), self.pagination, page)
            
            return [
                self.schema.dump(pagination.paginate(), many=True),
                {
                    'has_next': pagination.has_next(), 
                    "has_prev": pagination.has_prev()
                }
            ]

bp.add_url_rule('/index/<flag>/<int:page>',
                view_func=IndexView.as_view('index'))


class PersonView(MethodView):

    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, person_id):
        views = [
            ResumeView(), StaffView(), DocumentView(), ContactView(),
            AddressView(), WorkplaceView(), AffilationView(), RelationView(),
            CheckView(), PoligrafView(), InvestigationView(), InquiryView()
        ]
        
        results = await asyncio.gather(
            *[view.get(view_name, person_id) for view, view_name in zip(views, [
                'resume', 'staffs', 'documents', 'contacts', 'addresses', 'works',
                'affilations', 'relations', 'checks', 'poligafs', 'investigations', 'inquiries'
            ])]
        )
        return {'person': results}
    
bp.add_url_rule('/person/<int:person_id>', view_func=PersonView.as_view('person'))


class ResumeView(MethodView):
    
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    @bp.output(PersonSchema)
    async def get(self, action, person_id):
        async with async_session() as session:
            person = await session.get(Person, person_id)
            statuses = await session.execute(select(Status)).all()
            
            if action == 'status':
                person.status_id = statuses.filter_by(status=Statuses.new.value).first().id
                await session.commit()
                return session.execute(select(Person).filter_by(id=person_id)).first()
            
            elif action == 'send':
                status_ids = [
                    status.id for status in statuses 
                        if status.status in [Statuses.new.value, 
                                            Statuses.update.value, 
                                            Statuses.repeat.value]
                ]
                if person.has_status(status_ids):
                    anketa_schema = AnketaSchemaApi()
                    document = await session.execute(select(Document)). \
                            filter_by(person_id=person_id). \
                            order_by(Document.id.desc()).first(),
                    address = await session.execute(select(Address)). \
                            filter(Address.person_id == person_id,
                                Address.view.ilike("%регистрац%")). \
                            order_by(Address.id.desc()).first()
                    serial = anketa_schema.dump(
                        id=person.id,
                        fullname=person.fullname,
                        birthday=person.birthday,
                        birthplace=person.birthplace,
                        snils=person.snils,
                        inn=person.inn,
                        series=document.series,
                        number=document.number,
                        agency=document.agency,
                        issue=document.agency,
                        address=address.address
                        )
                    try:
                        async with aiohttp.ClientSession() as client_session:
                            async with client_session.post(url='https://httpbin.org/post', 
                                                           json=serial, 
                                                           timeout=5) as response:
                                response.raise_for_status()
                                
                                if response.status == 200:
                                    person.status_id = next((
                                        status.id for status in statuses \
                                            if status.status == Statuses.robot.value
                                    ), None)
                                    await session.add(Check(officer=current_user.fullname, 
                                                            person_id=person_id))
                                    await session.commit()
                                    return session.execute(select(Person))\
                                        .filter_by(id=person_id).first()
                                
                                return abort(response.status)
                    
                    except aiohttp.ClientError as e:
                        print(e)
                return abort(404)
            return person
        

    @roles_required(Roles.user.name, Roles.api.name)
    @bp.input(PersonSchema)
    async def post(self, action, json_data):
        person_id = await self.add_resume(json_data, action)
        return {'message': person_id}

    @roles_required(Roles.user.name)
    async def delete(self, action, person_id):
        async with async_session() as session:
            person = await session.get(Person, person_id)
            try:
                shutil.rmtree(os.path.join(current_app.config['BASE_PATH'], person.path))
            except Exception as e:
                print(e)
            await session.delete(person)
            await session.commit()
            return ''

    async def add_resume(self, resume: dict, action):
        """
        Adds a resume to the database.
        """
        async with async_session() as session:
            person = await session.execute(
                select(Person).filter(Person.fullname.ilike(resume['fullname']),
                                      Person.birthday==resume['birthday'])
                ).one_or_none()
        if person:
            statuses = await session.execute(select(Status)).scalars().all()
            status_id = statuses.filter_by(status=Statuses.new.value).first().id \
                if action in ["create", "api"] \
                    else statuses.filter_by(status=Statuses.update.value).first().id
            person.update(**resume)
            person.status_id = status_id
            person_id = person.id
        else:
            person = Person(**resume)
            await session.add(person)
            await session.flush()
            person_id = person.id

        person.path = self.make_folder(resume['fullname'], person_id)
        await session.commit()
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
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        async with async_session() as session:
            schema = StaffSchema()
            staffs = await session.execute(
                select(Staff).filter_by(person_id=item_id).order_by(Staff.id.desc())
            ).scalars()
            return await schema.dump(staffs, many=True)

    @bp.input(StaffSchema)
    @roles_required(Roles.user.value)
    async def post(self, action, item_id, json_data):
        async with async_session() as session:
            await session.add(Staff(**json_data | {'person_id': item_id}))
            await session.commit()
            return '', 201

    @bp.input(StaffSchema)
    @roles_required(Roles.user.value)
    async def patch(self, action, item_id, json_data):
        async with async_session() as session:
            staff = await session.get(Staff, person_id=item_id)
            staff.update(**json_data)
            await session.commit()
            return '', 201

    @roles_required(Roles.user.name)
    async def delete(self, action, item_id):
        async with async_session() as session:
            staff = await session.get(Staff, person_id=item_id)
            await session.delete(staff)
            await session.commit()
            return ''

bp.add_url_rule('/staff/<action>/<int:item_id>',
                view_func=StaffView.as_view('staff'))


class DocumentView(MethodView):

    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = DocumentSchema()
        async with async_session() as session:
            documents = await session.execute(
                select(Document).filter_by(person_id=item_id).order_by(Document.id.desc())
            ).scalars()
            return await schema.dump(documents, many=True)

    @roles_required(Roles.user.value)
    @bp.input(DocumentSchema)
    async def post(self, action, item_id, json_data):
        async with async_session() as session:
            await session.add(Document(**json_data | {'person_id': item_id}))
            await session.commit()
            return '', 201

    @roles_required(Roles.user.value)
    @bp.input(DocumentSchema)
    async def patch(self, action, item_id, json_data):
        async with async_session() as session:
            document = await session.get(Document, item_id)
            document.update(**json_data)
            await session.commit()
            return '', 201

    @roles_required(Roles.user.name)
    async def delete(self, action, item_id):
        async with async_session() as session:
            document = await session.get(Document, item_id)
            await session.delete(document)
            await session.commit()
            return ''

bp.add_url_rule('/document/<action>/<int:item_id>',
                view_func=DocumentView.as_view('document'))


class AddressView(MethodView):

    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = AddressSchema()
        async with async_session() as session:
            Address = await session.execute(
                select(Address).filter_by(person_id=item_id).order_by(Address.id.desc())
            ).scalars()
            return await schema.dump(Address, many=True)

    @roles_required(Roles.user.value)
    @bp.input(AddressSchema)
    async def post(self, action, item_id, json_data):
        async with async_session() as session:
            await session.add(Address(**json_data | {'person_id': item_id}))
            await session.commit()
            return '', 201

    @roles_required(Roles.user.value)
    @bp.input(AddressSchema)
    async def patch(self, action, item_id, json_data):
        async with async_session() as session:
            Address = await session.get(Address, item_id)
            Address.update(**json_data)
            await session.commit()
            return '', 201

    @roles_required(Roles.user.name)
    async def delete(self, action, item_id):
        async with async_session() as session:
            Address = await session.get(Address, item_id)
            await session.delete(Address)
            await session.commit()
            return ''

bp.add_url_rule('/address/<action>/<int:item_id>',
                view_func=AddressView.as_view('address'))


class ContactView(MethodView):

    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = ContactSchema()
        async with async_session() as session:
            Contact = await session.execute(
                select(Contact).filter_by(person_id=item_id).order_by(Contact.id.desc())
            ).scalars()
            return await schema.dump(Contact, many=True)

    @roles_required(Roles.user.value)
    @bp.input(ContactSchema)
    async def post(self, action, item_id, json_data):
        async with async_session() as session:
            await session.add(Contact(**json_data | {'person_id': item_id}))
            await session.commit()
            return '', 201

    @roles_required(Roles.user.value)
    @bp.input(ContactSchema)
    async def patch(self, action, item_id, json_data):
        async with async_session() as session:
            Contact = await session.get(Contact, item_id)
            Contact.update(**json_data)
            await session.commit()
            return '', 201

    @roles_required(Roles.user.name)
    async def delete(self, action, item_id):
        async with async_session() as session:
            Contact = await session.get(Contact, item_id)
            await session.delete(Contact)
            await session.commit()
            return ''

bp.add_url_rule('/contact/<action>/<int:item_id>',
                view_func=ContactView.as_view('contact'))


class WorkplaceView(MethodView):

    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = WorkplaceSchema()
        async with async_session() as session:
            Workplace = await session.execute(
                select(Workplace).filter_by(person_id=item_id).order_by(Workplace.id.desc())
            ).scalars()
            return await schema.dump(Workplace, many=True)
        
    @roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    async def post(self, action, item_id, json_data):
        json_data['now_work'] = bool(json_data.pop('now_work')) \
            if 'now_work' in json_data else False
        async with async_session() as session:
            await session.add(Workplace(**json_data | {'person_id': item_id}))
            await session.commit()
            return '', 201

    @roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    async def patch(self, action, item_id, json_data):
        json_data['now_work'] = bool(json_data.pop('now_work')) \
            if 'now_work' in json_data else False
        async with async_session() as session:
            Workplace = await session.get(Workplace, item_id)
            Workplace.update(**json_data)
            await session.commit()
            return '', 201

    @roles_required(Roles.user.name)
    async def delete(self, action, item_id):
        async with async_session() as session:
            Workplace = await session.get(Workplace, item_id)
            await session.delete(Workplace)
            await session.commit()
            return ''

bp.add_url_rule('/workplace/<action>/<int:item_id>',
                view_func=WorkplaceView.as_view('workplace'))


class RelationView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = RelationSchema()
        async with async_session() as session:
            Relation = await session.execute(
                select(Relation).filter_by(person_id=item_id).order_by(Relation.id.desc())
            ).scalars()
            return await schema.dump(Relation, many=True)
        
    @roles_required(Roles.user.value)
    @bp.input(RelationSchema)
    async def post(self, action, item_id, json_data):
        async with async_session() as session:
            await session.add(Relation(**json_data | {'person_id': item_id}))
            await session.add(Relation(relation=json_data['relation'],
                                       relation_id=item_id,
                                       person_id=json_data['relation_id']))
            await session.commit()
            return '', 201

    @roles_required(Roles.user.value)
    @bp.input(RelationSchema)
    async def patch(self, action, item_id, json_data):
        async with async_session() as session:
            Relation = await session.get(Relation, item_id)
            Relation.update(**json_data)
            await session.commit()
            return '', 201

    @roles_required(Roles.user.name)
    async def delete(self, action, item_id):
        async with async_session() as session:
            relaton = await session.get(Relation, item_id)
            await session.delete(relaton)
            await session.commit()
            return ''

bp.add_url_rule('/relation/<action>/<int:item_id>',
                view_func=RelationView.as_view('relation'))


class AffilationView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = AffilationSchema()
        async with async_session() as session:
            affilation = await session.execute(
                select(Affilation).filter_by(person_id=item_id).order_by(Affilation.id.desc())
            ).scalars()
            return await schema.dump(affilation, many=True)
        
    @roles_required(Roles.user.value)
    @bp.input(AffilationSchema)
    async def post(self, action, item_id, json_data):
        async with async_session() as session:
            await session.add(Affilation(**json_data | {'person_id': item_id}))
            await session.commit()
            return '', 201

    @roles_required(Roles.user.value)
    @bp.input(AffilationSchema)
    async def patch(self, action, item_id, json_data):
        async with async_session() as session:
            affilation = await session.get(Affilation, item_id)
            affilation.update(**json_data)
            await session.commit()
            return '', 201

    @roles_required(Roles.user.name)
    async def delete(self, action, item_id):
        async with async_session() as session:
            affilation = await session.get(Affilation, item_id)
            await session.delete(affilation)
            await session.commit()
            return ''

bp.add_url_rule('/affilation/<action>/<int:item_id>',
                view_func=AffilationView.as_view('affilation'))


class CheckView(MethodView):

    async def __init__(self):
        async with async_session() as session:
            self.statuses = await session.execute(select(Status)).all()
    
    @group_required(Groups.staffsec.name)
    @bp.doc(hide=True)
    async def get(self, action, item_id):
        async with async_session() as session:
            if action == 'add':
                    status_ids = [
                        status.id for status in self.statuses 
                            if status.status in [Statuses.new.value, 
                                                Statuses.update.value, 
                                                Statuses.repeat.value]
                    ]
                    person = await session.execute(Person).get(item_id)
                    if person.has_status(status_ids):
                        person.status_id = self.statuses.filter(
                            Status.status == Statuses.manual.value).first().id
                        await session.add(Check(officer=current_user.fullname,
                                                person_id=item_id))
                        await session.commit()
                        return '', 201

            if action == 'self':
                check = session.execute(select(Check)
                                        .filter_by(person_id=item_id)
                                        .order_by(Check.id.desc())).first()
                old_officer_id = await session.execute(
                    select(User).filter_by(fullname=check.officer)
                    ).scalar()
                check.officer = current_user.fullname
                await session.add(Message(
                    category=Statuses.new.value,
                    report=f'Анкета делегирована {current_user.fullname}', 
                            user_id=old_officer_id))
                await session.commit()
                return '', 201
        schema = CheckSchema()
        return schema.dump(session.execute(Check). \
                        filter_by(person_id=item_id). \
                        order_by(Check.id.desc()).all(), many=True)

    @roles_required(Roles.api.name)
    @bp.doc(hide=False)
    @bp.input(CheckSchemaApi)
    async def post(self, json_data):
        async with async_session() as session:
            candidate = await session.get(Person, json_data['id'])
            del json_data['id']
            latest_check = session.execute(select(Check)
                                           .filter_by(person_id=candidate.id)
                                           .order_by(Check.id.desc())).first()
            user = session.execute(User).filter_by(fullname=latest_check.officer).one_or_none()
            
            if candidate.status_id == self.statuses.filter(Status.status == Statuses.robot.value).first().id:
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
                        await session.add(Message(report=f'{error}', user_id=user.id))

                await latest_check.update(**json_data)
                await session.add(Message(report=f'Проверка кандидата \
                                        {candidate.fullname} окончена', user_id=user.id))
                candidate.status_id = self.statuses.filter(Status.status == Statuses.reply.value).first().id
                await session.commit()

            else:
                await session.add(Message(
                    report=f'Результат проверки'
                           f'{candidate.fullname} не может быть записан.'
                           f'Материал проверки находится в {json_data["path"]}', 
                          user_id=user.id))
                await session.commit()

            return '', 201
    
    @roles_required(Roles.user.value)
    @bp.input(CheckSchema)
    @bp.doc(hide=True)
    async def patch(self, action, item_id, json_data):
        async with async_session() as session:
            conclusions = await session.execute(select(Conclusion)).all()
            json_data['pfo'] = bool(json_data.pop('pfo')) if 'pfo' in json_data else False
            if action == 'create':
                person = await session.get(Person, item_id)
                await session.add(Check(
                    **json_data | {'person_id': item_id,
                    'officer': current_user.fullname})
                    )
            else:
                check = await session.get(Check, item_id)
                person = await session.get(Person, check.person_id)
                await check.update(**json_data)
            conclusion_saved_id = next(c.id for c in conclusions 
                                       if c.conclusion == Conclusions.saved.value)
            status_save_id = next(s.id for s in self.statuses 
                                  if s.status == Statuses.save.value)
            status_poligraf_id = next(s.id for s in self.statuses 
                                      if s.status == Statuses.poligraf.value)
            status_finish_id = next(s.id for s in self.statuses 
                                    if s.status == Statuses.finish.value)
            if json_data['conclusion_id'] == conclusion_saved_id:
                person.status_id = status_save_id
            else:
                person.status_id = status_poligraf_id \
                    if json_data['pfo'] else status_finish_id
            await session.commit()
            return '', 201

    @roles_required(Roles.user.name)
    @bp.doc(hide=True)
    async def delete(self, action, item_id):
        async with async_session() as session:
            check = await session.get(Check, item_id)
            person = await session.get(Person, check.person_id)
            person.status = self.statuses.filter(Status.status == Statuses.update.value).first().id
            await session.delete(check)
            await session.commit()
            return ''

bp.add_url_rule('/check/<action>/<int:item_id>',
                view_func=CheckView.as_view('check'))


class InvestigationView(MethodView):
    """The InvestigationView class is a subclass of the MethodView class from the flask.views module.
    """
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        async with async_session() as session:
            schema = InvestigationSchema()
            investigations = await session.execute(
                select(Investigation)
                .filter_by(person_id=item_id)
                .order_by(Investigation.id.desc())
            ).scalars()
            return await schema.dump(investigations, many=True)
        
    @roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    async def post(self, action, item_id, json_data):
        async with async_session() as session:
            await session.add(Investigation(**json_data | {'person_id': item_id}))
            await session.commit()
            return '', 201

    @roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    async def patch(self, action, item_id, json_data):
        async with async_session() as session:
            invs = await session.get(Investigation, item_id)
            invs.update(**json_data)
            await session.commit()
            return '', 201

    @roles_required(Roles.user.name)
    async def delete(self, action, item_id):
        async with async_session() as session:
            investigation = await session.get(Investigation, item_id)
            await session.delete(investigation)
            await session.commit()
            return ''

bp.add_url_rule('/investigation/<action>/<int:item_id>',
                view_func=InvestigationView.as_view('investigation'))


class PoligrafView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        async with async_session() as session:
            schema = PoligrafSchema()
            poligrafs = await session.execute(
                select(Poligraf)
                .filter_by(person_id=item_id)
                .order_by(Poligraf.id.desc())
            ).scalars()
            return await schema.dump(poligrafs, many=True)
        
    @roles_required(Roles.user.value)
    @bp.input(PoligrafSchema)
    async def post(self, action, item_id, json_data):
        async with async_session() as session:
            statuses = await session.execute(select(Status)).all()
            person = await session.get(Person, item_id)
            if person.has_status(statuses.filter_by(status=Statuses.poligraf.value).first().id):
                person.status = statuses.filter_by(status=Statuses.finish.value).first().id
            await session.add(Poligraf(
                **json_data | {'person_id': item_id,
                'officer': current_user.fullname}
                ))
            await session.commit()
            return '', 201

    @roles_required(Roles.user.value)
    @bp.input(PoligrafSchema)
    async def patch(self, action, item_id, json_data):
        async with async_session() as session:
            poligraf = await session.get(Poligraf, item_id)
            poligraf.update(**json_data)
            await session.commit()
            return '', 201

    @roles_required(Roles.user.name)
    async def delete(self, action, item_id):
        async with async_session() as session:
            pfo = await session.get(Poligraf, item_id)
            await session.delete(pfo)
            await session.commit()
            return ''

bp.add_url_rule('/poligraf/<action>/<int:item_id>',
                view_func=PoligrafView.as_view('poligraf'))


class InquiryView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        async with async_session() as session:
            schema = InquirySchema()
            inquiries = await session.execute(
                select(Inquiry)
                .filter_by(person_id=item_id)
                .order_by(Inquiry.id.desc())
            ).scalars()
            return await schema.dump(inquiries, many=True)
        
    @bp.input(InquirySchema)
    @roles_required(Roles.user.value)
    async def post(self, action, item_id, json_data):
        async with async_session() as session:
            await session.add(Inquiry(**json_data | {'person_id': item_id}))
            await session.commit()
            return '', 201

    @bp.input(InquirySchema)
    @roles_required(Roles.user.value)
    async def patch(self, action, item_id, json_data):
        async with async_session() as session:
            inquiry = await session.get(Inquiry, item_id)
            inquiry.update(**json_data)
            await session.commit()
            return '', 201

    @roles_required(Roles.user.name)
    async def delete(self, action, item_id):
        async with async_session() as session:
            pfo = await session.get(Inquiry, item_id)
            await session.delete(pfo)
            await session.commit()
            return ''

bp.add_url_rule('/inquiry/<action>/<int:item_id>',
                view_func=InquiryView.as_view('inquiry'))


class InfoView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def post(self):
        response = request.get_json()
        async with async_session() as session:
            candidates = session.execute(
                extract('month', Check.deadline).label('month'),
                Check.conclusion,
                func.count(Check.id)
            ). \
                join(Person, Person.id == Check.person_id). \
                group_by(Check.conclusion, extract('month', Check.deadline)). \
                filter(and_(Check.deadline.between(response['start'],
                                                    response['end']), 
                            Person.region_id == int(response['region']))).all()

            pfo = session.execute(Poligraf.theme, func.count(Poligraf.id)). \
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

    decorators = [group_required(Groups.staffsec.name),
                  roles_required(Roles.user.name),
                  bp.doc(hide=True)]

    async def get(self, action, item_id):
        """
        Retrieves a file from the server and sends it as a response.
        Parameters:
            action (str): The action to perform.
            item_id (int): The ID of the item to retrieve.
        Returns:
            FileResponse: The file response containing the requested file, if it exists.
        """
        async with async_session() as session:
            person = await session.get(Person, item_id)
            file_path = os.path.join(current_app.config['BASE_PATH'], 
                                    person.path, 'images', 'image.jpg')
            if os.path.isfile(file_path):
                return await send_file(file_path, as_attachment=True)
            return await abort(404)

    async def post(self, action, item_id=0):

        if not request.files['file'].filename:
            return {'result': False, 'item_id': item_id}

        async with async_session() as session:
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
                            await session.add(model(**item | {'person_id': person_id}))

                person = await session.get(Person, person_id)
                if person.path:
                    full_path = os.path.join(current_app.config["BASE_PATH"], person.path)
                    if not os.path.isdir(full_path):
                        os.mkdir(full_path)
                else:
                    person.path = resume_view.make_folder(person.fullname, person_id)
                await session.commit()

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
                item = await session.get(model, item_id)
                person = await session.get(Person, item.person_id)
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