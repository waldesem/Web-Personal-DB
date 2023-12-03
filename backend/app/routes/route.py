import asyncio
import os
import requests
import shutil
from datetime import datetime

from apiflask import abort, EmptySchema
from flask import request, current_app, send_file
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy import select, and_, extract, func
from werkzeug.utils import secure_filename
from PIL import Image
import aiohttp


from . import bp
from .login import roles_required, group_required
from ..utils.jsonparser import JsonFile
from ..models.model import  Category, User, Person, Staff, Document, Address, Contact, \
    Workplace, Check, Poligraf, Investigation, Inquiry, Relation, \
    Status, Report, Affilation, async_session
from ..models.schema import RelationSchema, StaffSchema, AddressSchema, \
    PersonSchema, ContactSchema, DocumentSchema, CheckSchema, InquirySchema, \
    InvestigationSchema, PoligrafSchema, AnketaSchemaApi, \
    WorkplaceSchema, AffilationSchema, CheckSchemaApi
from ..models.classes import Categories, Roles, Groups, Statuses


class IndexView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def __init__(self) -> None:
        self.pagination = 16
        self.schema = PersonSchema()

    async def post(self, flag, page):
        json_data = request.get_json()
        async with async_session() as session:
            query = await session.execute(select(Person)).order_by(Person.id.desc())
            categories = await session.execute(select(Category)).all()
            statuses = await session.execute(select(Status)).all()
        match flag:
            case 'new':
                query = query.filter(Person.status.in_([
                    statuses.filter_by(status=Statuses.new.value).first().id,
                    statuses.filter_by(status=Statuses.repeat.value).first().id,
                    statuses.filter_by(status=Statuses.update.value).first().id
                    ]),
                    Person.category == categories.filter_by(category=Categories.candidate.name).\
                        filter_by(category=Categories.candidate.name
                    ))
            case 'officer':
                query = query.filter(Person.status.notin_([
                    statuses.filter_by(status=Statuses.finish.value).first().id,
                    statuses.filter_by(status=Statuses.cancel.value).first().id
                    ])) \
                    .join(Check, isouter=True) \
                    .filter_by(officer=current_user.fullname)
            case 'search':
                if json_data['search']:
                    query = await Person.query.search('%{}%'.format(json_data['search'])) 
                    
        result = query.paginate(page=page,
                                per_page=self.pagination,
                                error_out=False)
        
        has_next, has_prev = bool(result.has_next), bool(result.has_prev)
        
        return [self.schema.dump(result, many=True),
                {'has_next': has_next, "has_prev": has_prev}]

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
    
bp.add_url_rule('/person/<int:person_id>', PersonView.as_view('person'))


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
            
            elif action == 'delegate':
                async with async_session() as session:
                    check = session.execute(select(Check)
                                            .filter_by(person_id=person_id)
                                            .order_by(Check.id.desc())).first()
                    old_officer_id = await session.execute(
                        select(User).filter_by(fullname=check.officer)
                        ).scalar()
                    check.officer = current_user.fullname
                    await session.add(Report(
                        category=Statuses.new.value,
                        report=f'Анкета #{person_id} делегирована'
                                f'{current_user.fullname}', user_id=old_officer_id))
                    await session.commit()
                    return '', 201
            return person
        

    @roles_required(Roles.user.name, Roles.api.name)
    @bp.input(PersonSchema)
    async def post(self, action, json_data):
        person_id = await self.add_resume(json_data, action)
        return {'message': person_id}

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
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
            person.update(resume)
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
        schema = StaffSchema()
        return schema.dump(session.execute(Staff). \
                           filter_by(person_id=item_id). \
                           order_by(Staff.id.desc()).all(), many=True)

    @bp.input(StaffSchema)
    @roles_required(Roles.user.value)
    async def post(self, action, item_id, json_data):
        db.session.add(Staff(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201

    @bp.input(StaffSchema)
    @roles_required(Roles.user.value)
    async def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(session.execute(Staff).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    async def delete(self, action, item_id):
        db.session.delete(session.execute(Staff).get(item_id))
        db.session.commit()
        return ''


bp.add_url_rule('/staff/<action>/<int:item_id>',
                view_func=StaffView.as_view('staff'))


class DocumentView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = DocumentSchema()
        return schema.dump(session.execute(Document). \
                           filter_by(person_id=item_id). \
                           order_by(Document.id.desc()).all(), many=True)

    @roles_required(Roles.user.value)
    @bp.input(DocumentSchema)
    async def post(self, action, item_id, json_data):
        db.session.add(Document(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.value)
    @bp.input(DocumentSchema)
    async def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(session.execute(Document).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    async def delete(self, action, item_id):
        db.session.delete(session.execute(Document).get(item_id))
        db.session.commit()
        return ''


bp.add_url_rule('/document/<action>/<int:item_id>',
                view_func=DocumentView.as_view('document'))


class AddressView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = AddressSchema()
        return schema.dump(session.execute(Address). \
                           filter_by(person_id=item_id). \
                           order_by(Address.id.desc()).all(), many=True)

    @roles_required(Roles.user.value)
    @bp.input(AddressSchema)
    async def post(self, action, item_id, json_data):
        db.session.add(Address(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.value)
    @bp.input(AddressSchema)
    async def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(session.execute(Address).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    async def delete(self, action, item_id):
        db.session.delete(session.execute(Address).get(item_id))
        db.session.commit()
        return ''


bp.add_url_rule('/address/<action>/<int:item_id>',
                view_func=AddressView.as_view('address'))


class ContactView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = ContactSchema()
        return schema.dump(session.execute(Contact). \
                           filter_by(person_id=item_id). \
                           order_by(Contact.id.desc()).all(), many=True)

    @roles_required(Roles.user.value)
    @bp.input(ContactSchema)
    async def post(self, action, item_id, json_data):
        db.session.add(Contact(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.value)
    @bp.input(ContactSchema)
    async def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(session.execute(Contact).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    async def delete(self, action, item_id):
        db.session.delete(session.execute(Contact).get(item_id))
        db.session.commit()
        return ''

bp.add_url_rule('/contact/<action>/<int:item_id>',
                view_func=ContactView.as_view('contact'))


class WorkplaceView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = WorkplaceSchema()
        return schema.dump(session.execute(Workplace). \
                           filter_by(person_id=item_id). \
                           order_by(Workplace.id.desc()).all(), many=True)

    @roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    async def post(self, action, item_id, json_data):
        json_data['now_work'] = bool(json_data.pop('now_work')) \
            if 'now_work' in json_data else False
        db.session.add(Workplace(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.value)
    @bp.input(WorkplaceSchema)
    async def patch(self, action, item_id, json_data):
        json_data['now_work'] = bool(json_data.pop('now_work')) \
            if 'now_work' in json_data else False
        for k, v in json_data.items():
            setattr(session.execute(Workplace).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    async def delete(self, action, item_id):
        db.session.delete(session.execute(Workplace).get(item_id))
        db.session.commit()
        return ''

bp.add_url_rule('/workplace/<action>/<int:item_id>',
                view_func=WorkplaceView.as_view('workplace'))


class RelationView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = RelationSchema()
        return schema.dump(session.execute(Relation). \
                           filter_by(person_id=item_id). \
                           order_by(Relation.id.desc()).all(), many=True)

    @roles_required(Roles.user.value)
    @bp.input(RelationSchema)
    async def post(self, action, item_id, json_data):
        db.session.add(Relation(**json_data | {'person_id': item_id}))
        db.session.add(Relation(relation=json_data['relation'],
                                relation_id=item_id,
                                person_id=json_data['relation_id']))
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.value)
    @bp.input(RelationSchema)
    async def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(session.execute(Relation).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    async def delete(self, action, item_id):
        db.session.delete(session.execute(Relation).get(item_id))
        db.session.commit()
        return ''


bp.add_url_rule('/relation/<action>/<int:item_id>',
                view_func=RelationView.as_view('relation'))


class AffilationView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = AffilationSchema()
        return schema.dump(session.execute(Affilation). \
                           filter_by(person_id=item_id). \
                           order_by(Affilation.id.desc()).all(), many=True)

    @roles_required(Roles.user.value)
    @bp.input(AffilationSchema)
    async def post(self, action, item_id, json_data):
        db.session.add(Affilation(**json_data | {'person_id': item_id}))
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.value)
    @bp.input(AffilationSchema)
    async def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(session.execute(Affilation).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    async def delete(self, action, item_id):
        db.session.delete(session.execute(Affilation).get(item_id))
        db.session.commit()
        return ''

bp.add_url_rule('/affilation/<action>/<int:item_id>',
                view_func=AffilationView.as_view('affilation'))


class CheckView(MethodView):
    
    @group_required(Groups.staffsec.name)
    @bp.doc(hide=True)
    async def get(self, action, item_id):
        if action == 'add':
            person = session.execute(Person).get(item_id)
            if person.has_status([Status.new.value,
                                  Status.update.value,
                                  Status.repeat.value]):
                person.status = Status.manual.value
                db.session.add(Check(officer=current_user.fullname,
                                     person_id=item_id))
                db.session.commit()
                return '', 201

        if action == 'self':
            check = session.execute(Check).get(item_id)
            prev_officer = session.execute(User).\
                filter_by(fullname=check.officer).one_or_none()
            new_officer = session.execute(User).\
                filter_by(fullname=current_user.fullname).one_or_none()
            db.session.add(Report(category=Reports.high.value, 
                                  report=f'Aнкета ID #{id} делегирована {current_user.fullname}', user_id=prev_officer.id))
            check.officer = current_user.fullname
            db.session.add(Report(category=Reports.high.value, 
                                  report=f'Aнкета ID #{id} переделегирована {current_user.fullname}', user_id=new_officer.id))
            db.session.commit()
            return '', 201

        schema = CheckSchema()
        return schema.dump(session.execute(Check). \
                           filter_by(person_id=item_id). \
                           order_by(Check.id.desc()).all(), many=True)

    @roles_required(Roles.api.name)
    @bp.doc(hide=False)
    @bp.input(CheckSchemaApi)
    async def post(json_data):
        candidate = session.execute(Person).get(json_data['id'])
        del json_data['id']
        latest_check = session.execute(Check).filter_by(person_id=candidate.id).\
            order_by(Check.id.desc()).first()
        user = session.execute(User).filter_by(fullname=latest_check.officer).one_or_none()
        
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
    
    @roles_required(Roles.user.value)
    @bp.input(CheckSchema)
    @bp.doc(hide=True)
    async def patch(self, action, item_id, json_data):
        json_data['pfo'] = bool(json_data.pop('pfo')) if 'pfo' in json_data else False
        if action == 'create':
            person = session.execute(Person).get(item_id)
            db.session.add(Check(**json_data | {'person_id': item_id,
                                                'officer': current_user.fullname}))
        else:
            check = session.execute(Check).get(item_id)
            person = session.execute(Person).get(check.person_id)
            for k, v in json_data.items():
                setattr(check, k, v)
        if json_data['conclusion'] == (Status.save.value).upper():
            person.status = Status.save.value
        else:
            person.status = Status.poligraf.value if json_data['pfo'] \
                else Status.result.value
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    @bp.doc(hide=True)
    async def delete(self, action, item_id):
        check = session.execute(Check).get(item_id)
        try:
            shutil.rmtree(os.path.join(current_app.config['BASE_PATH'], check.path))
        except Exception as e:
            print(e)
        person = session.execute(Person).get(session.execute(Check.person_id). \
                                              filter_by(id=item_id).one_or_none())
        person.status = Status.update.value
        db.session.delete(check)
        db.session.commit()
        return ''


bp.add_url_rule('/check/<action>/<int:item_id>',
                view_func=CheckView.as_view('check'))


class InvestigationView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = InvestigationSchema()
        return schema.dump(session.execute(Investigation). \
                           filter_by(person_id=item_id). \
                           order_by(Investigation.id.desc()).all(), many=True)

    @roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    async def post(self, action, item_id, json_data):
        db.session.add(Investigation(**json_data | {'person_id': item_id,
                                                    'officer': current_user.fullname}))
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.value)
    @bp.input(InvestigationSchema)
    async def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(session.execute(Investigation).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    async def delete(self, action, item_id):
        invs = session.execute(Investigation).get(item_id)
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
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = PoligrafSchema()
        return schema.dump(session.execute(Poligraf). \
                           filter_by(person_id=item_id). \
                           order_by(Poligraf.id.desc()).all(), many=True)

    @roles_required(Roles.user.value)
    @bp.input(PoligrafSchema)
    async def post(self, action, item_id, json_data):
        person = session.execute(Person).get(item_id)
        if person.has_status(Status.poligraf.value):
            person.status = Status.result.value
        db.session.add(Poligraf(**json_data | {'person_id': item_id,
                                               'officer': current_user.fullname}))
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.value)
    @bp.input(PoligrafSchema)
    async def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(session.execute(Poligraf).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    async def delete(self, action, item_id):
        pfo = session.execute(Poligraf).get(item_id)
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
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def get(self, action, item_id):
        schema = InquirySchema()
        return schema.dump(session.execute(Inquiry). \
                           filter_by(person_id=item_id). \
                           order_by(Inquiry.id.desc()).all(), many=True)

    @bp.input(InquirySchema)
    @roles_required(Roles.user.value)
    async def post(self, action, item_id, json_data):
        db.session.add(Inquiry(**json_data | {'person_id': item_id,
                                              'officer': current_user.fullname}))
        db.session.commit()
        return '', 201

    @bp.input(InquirySchema)
    @roles_required(Roles.user.value)
    async def patch(self, action, item_id, json_data):
        for k, v in json_data.items():
            setattr(session.execute(Inquiry).get(item_id), k, v)
        db.session.commit()
        return '', 201

    @roles_required(Roles.user.name)
    @bp.output(EmptySchema, status_code=204)
    async def delete(self, action, item_id):
        db.session.delete(session.execute(Inquiry).get(item_id))
        db.session.commit()
        return ''

bp.add_url_rule('/inquiry/<action>/<int:item_id>',
                view_func=InquiryView.as_view('inquiry'))


class InfoView(MethodView):
    decorators = [group_required(Groups.staffsec.name), bp.doc(hide=True)]

    async def post(self):
        response = request.get_json()

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
        person = session.execute(Person).get(item_id)
        file_path = os.path.join(current_app.config['BASE_PATH'], 
                                 person.path, 'images', 'image.jpg')
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True)
        return abort(404)

    async def post(self, action, item_id=0):

        if not request.files['file'].filename:
            return {'result': False, 'item_id': item_id}

        resume_view = ResumeView()
        if action == 'anketa':
            location_id = session.execute(User.region_id). \
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

            person = session.execute(Person).get(person_id)
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
            item = session.execute(model).filter_by(id=item_id).scalar()
            person = session.execute(Person).get(item.person_id)
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