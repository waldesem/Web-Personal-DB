from datetime import datetime
import os
import shutil

import httpx
from apiflask import EmptySchema
from flask import abort, request, send_file
from flask.views import MethodView
from flask_jwt_extended import current_user
from werkzeug.utils import secure_filename
from sqlalchemy_searchable import search
from sqlalchemy import func, select
from PIL import Image

from config import Config
from . import bp
from .login import roles_required
from ..utils.folders import create_folders
from ..utils.jsonparser import parse_json
from ..models.classes import Roles, Conclusions, Statuses
from ..models.model import (
    db,
    Staff,
    Document,
    Address,
    Contact,
    Workplace,
    Relation,
    Affilation,
    Conclusion,
    Person,
    Check,
    Poligraf,
    Investigation,
    Inquiry,
    Status,
    Message,
    Robot,
)
from ..models.schema import (
    ActionSchema,
    AnketaSchemaApi,
    InfoSchema,
    PersonSchema,
    RelationSchema,
    StaffSchema,
    AddressSchema,
    ContactSchema,
    DocumentSchema,
    WorkplaceSchema,
    AffilationSchema,
    CheckSchema,
    InquirySchema,
    InvestigationSchema,
    PoligrafSchema,
    RobotSchema,
    SearchSchema,
    ModelSchema,
)


@roles_required(Roles.user.value)
@bp.doc(hide=True)
@bp.route("/image/<int:item_id>")
def get_image(item_id):
    """
    Retrieves a file from the server and sends it as a response.
    """
    person = db.session.get(Person, item_id)
    if person.path:
        file_path = os.path.join(Config.BASE_PATH, person.path, "image", "image.jpg")
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file(Config.NO_PHOTO, as_attachment=True, mimetype="image/jpg")


@roles_required(Roles.user.value)
@bp.get("/information")
@bp.input(InfoSchema, location="query")
def get_information(query_data):
    candidates = db.session.execute(
        select(Check.conclusion_id, func.count(Check.id))
        .join(Person)
        .group_by(Check.conclusion_id)
        .filter(Person.region_id == query_data["region_id"])
        .filter(Check.deadline.between(query_data["start"], query_data["end"]))
    ).all()
    return dict(map(lambda x: (x[1], x[0]), candidates)), 200


class IndexView(MethodView):

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    @bp.input(SearchSchema, location="query")
    def get(self, flag, page, query_data):
        search_data = query_data.get("search")
        query = select(Person).order_by(Person.id.desc())
        if flag != "search":
            match flag:
                case "new":
                    query = query.filter(
                        Person.status_id.in_(
                            [
                                Status().get_id(Statuses.new.value),
                                Status().get_id(Statuses.update.value),
                                Status().get_id(Statuses.repeat.value),
                            ]
                        ),
                    )
                case "officer":
                    query = query.filter(
                        Person.status_id.notin_(
                            [
                                Status().get_id(Statuses.finish.value),
                                Status().get_id(Statuses.cancel.value),
                            ]
                        ),
                        Person.user_id == current_user.id,
                    )
        else:
            if search_data:
                query = search(query, "%{}%".format(search_data))

        result = db.paginate(query, page=page, per_page=16, error_out=False)
        return [
            PersonSchema().dump(result, many=True),
            {"has_next": bool(result.has_next), "has_prev": bool(result.has_prev)},
        ]


index_view = IndexView.as_view("index")
bp.add_url_rule("/index/<flag>/<int:page>", view_func=index_view)


class ResumeView(MethodView):

    decorators = [roles_required(Roles.user.value), bp.doc(hide=True)]

    @bp.input(ActionSchema, location="query")
    def get(self, person_id, query_data):
        action = query_data.get("action")
        person = db.session.get(Person, person_id)
        if person:
            if action == "status":
                person.status_id = Status.get_id(Statuses.update.value)
                person.user_id = None
                db.session.commit()
                return self.get(person_id), 201

            if action == "self":
                if not person.user_id:
                    db.session.add(
                        Message(
                            message=f"Aнкета ID #{person_id} принята в работу",
                            user_id=current_user.id,
                        )
                    )
                    person.status_id = Status.get_id(Statuses.manual.value)

                    person.user_id = current_user.id
                    db.session.commit()
                    return "", 201
            elif action == "send":
                if person.status_id in (
                    Status.get_id(Statuses.new.value),
                    Status.get_id(Statuses.update.value),
                    Status.get_id(Statuses.repeat.value),
                ):
                    docum = db.session.execute(
                        select(Document)
                        .filter_by(person_id=person_id)
                        .order_by(Document.id.desc())
                    ).scalar_one_or_none()
                    addr = db.session.execute(
                        select(Address)
                        .filter(
                            Address.person_id == person_id,
                            Address.view.ilike("%регистрац%"),
                        )
                        .order_by(Address.id.desc())
                    ).scalar_one_or_none()
                    serial = AnketaSchemaApi().dump(
                        {
                            "id": person_id,
                            "surname": person.surname,
                            "firstname": person.firstname,
                            "patronymic": person.patronymic,
                            "birthday": person.birthday,
                            "birthplace": person.birthplace,
                            "snils": person.snils,
                            "inn": person.inn,
                            "series": docum.series,
                            "number": docum.number,
                            "agency": docum.agency,
                            "issue": docum.issue,
                            "address": addr.address,
                            "user_id": current_user.id,
                        }
                    )
                    try:
                        response = httpx.post(
                            url="https://httpbin.org/post", json=serial, timeout=5
                        )
                        response.raise_for_status()
                        person.status_id = Status.get_id(Statuses.robot.value)
                        person.user_id = current_user.id
                        db.session.commit()
                        return self.get(person_id)
                    except httpx.HTTPError as exc:
                        print(f"Error while requesting {exc.request.url!r}.")
                return abort(403)
            return PersonSchema().dump(person), 201
        return abort(403)

    @bp.output(EmptySchema)
    def delete(self, person_id):
        person = db.session.get(Person, person_id)
        db.session.delete(person)
        db.session.commit()
        return "", 204

    @bp.input(PersonSchema)
    def patch(self, person_id, json_data):
        person = db.session.get(Person, person_id)
        for k, v in json_data.items():
            setattr(person, k, v)
            db.session.commit()
        return {"message": person_id}

    @bp.input(PersonSchema)
    def post(self, action, json_data):
        person_id = ResumeView.add_resume(json_data, action)
        return {"message": person_id}

    @staticmethod
    def add_resume(resume: dict, action):
        """
        Adds a resume to the database.
        """
        person = db.session.execute(
            select(Person).filter(
                Person.surname.ilike(resume["surname"]),
                Person.firstname.ilike(resume["firstname"]),
                Person.patronymic.ilike(f"%{resume.get('patronymic')}%"),
                Person.birthday == resume["birthday"],
            )
        ).one_or_none()

        resume["surname"] = resume["surname"].strip().upper()
        resume["firstname"] = resume["firstname"].strip().upper()
        resume["patronymic"] = resume.get("patronymic", "").strip().upper()

        if person:
            person_id = person.id
            for k, v in resume.items():
                setattr(person, k, v)
        else:
            if action == "create":
                resume["status_id"] = Status().get_id(Statuses.manual.value)
                resume["user_id"] = current_user.id
            if action == "api":
                resume["status_id"] = Status().get_id(Statuses.new.value)

            person = Person(**resume)
            db.session.add(person)
            db.session.flush()
            person_id = person.id

        person.path = os.path.join(
            resume["surname"][0].upper(),
            f"{person_id}-{resume['surname']} {resume['firstname']} {resume.get('patronymic', '')}".rstrip(),
        )
        url = os.path.join(Config.BASE_PATH, person.path)
        if not os.path.isdir(url):
            os.mkdir(url)
        person.user_id = current_user.id
        db.session.commit()
        return person_id


resume_view = ResumeView.as_view("resume")
bp.add_url_rule(
    "/resume/<action>",
    view_func=resume_view,
    methods=["POST"],
)
bp.add_url_rule(
    "/resume/<int:person_id>",
    view_func=resume_view,
    methods=["GET", "DELETE", "PATCH"],
)


class ItemsView(MethodView):

    models_schemas = {
        "staff": [Staff, StaffSchema()],
        "document": [Document, DocumentSchema()],
        "address": [Address, AddressSchema()],
        "contact": [Contact, ContactSchema()],
        "workplace": [Workplace, WorkplaceSchema()],
        "relation": [Relation, RelationSchema()],
        "affilation": [Affilation, AffilationSchema()],
        "check": [Check, CheckSchema()],
        "robot": [Robot, RobotSchema()],
        "poligraf": [Poligraf, PoligrafSchema()],
        "investigation": [Investigation, InvestigationSchema()],
        "inquiry": [Inquiry, InquirySchema()],
    }

    def __init__(self):
        self.model = None
        self.schema = None

    def defines(self, item):
        self.model = ItemsView.models_schemas[item][0]
        self.schema = ItemsView.models_schemas[item][1]

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def get(self, item, item_id):
        self.defines(item)
        query = (
            select(self.model)
            .filter_by(person_id=item_id)
            .order_by(self.model.id.desc())
        )
        result = db.session.execute(query).scalars().all()
        return self.schema().dump(result, many=True), 200

    @roles_required(Roles.user.value, Roles.api.value)
    @bp.doc(hide=True)
    def post(self, item, item_id):
        self.defines(item)
        resp = request.get_json()
        json_data = self.schema.load(resp)

        if item == 'workplace':
            json_data["now_work"] = (
            bool(json_data.pop("now_work")) if "now_work" in json_data else False
            )

        if item == 'check':
            json_data["pfo"] = (
                bool(json_data.pop("pfo")) if "pfo" in json_data else False
            )

        json_data = json_data | {"person_id": item_id}
        if item in ['check', 'poligraf', 'inquiry', 'investigation']:
            json_data | {"officer": current_user.fullname}
        
        result = self.model(json_data)

        if item == 'relation':
            db.session.add(
            Relation(
                relation=json_data["relation"],
                relation_id=item_id,
                person_id=json_data["relation_id"],
            )
        )
            
        if item == "check":
            person = db.session.get(Person, item_id)
            if json_data["conclusion_id"] == Conclusion.get_id(Conclusions.saved.value):
                person.status_id = Status.get_id(Statuses.save.value)
            else:
                person.status_id = (
                    Status.get_id(Statuses.poligraf.value)
                    if json_data["pfo"]
                    else Status.get_id(Statuses.finish.value)
                )
                person.user_id = None

        if item == "poligraf":
            person = db.session.get(Person, item_id)
            if person.status_id == Status.get_id(Statuses.poligraf.value):
                person.status_id = Status.get_id(Statuses.finish.value)

        if item == "robot":
            self.post_robot(json_data)
        else:
            db.session.add(result)
            db.session.commit()
            return "", 201

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def patch(self, item, item_id):
        self.defines(item)
        resp = request.get_json()
        json_data = self.schema.load(resp)
        if item == 'workplace':
            json_data["now_work"] = (
            bool(json_data.pop("now_work")) if "now_work" in json_data else False
        )
        result = db.session.get(self.model, item_id)
        if result:
            for k, v in json_data.items():
                setattr(result, k, v)
            db.session.commit()
            return "", 201
        return abort(403)

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def delete(self, item, item_id):
        self.defines(item)
        result = db.session.get(self.model, item_id)
        if result:
            db.session.delete(result)
            if item == "check":
                person = db.session.get(Person, result.person_id)
                person.status = Status.get_id(Statuses.update.value)
                person.user_id = ""
            db.session.commit()
            return "", 204
        return abort(403)

    def post_robot(json_data):
        user_id = json_data.pop("user_id")
        robot_path = json_data.pop("path")
        candidate = db.session.get(Person, json_data["id"])

        del json_data["id"]

        if candidate.status_id == Status.get_id(Statuses.robot.value):
            if os.path.isdir(json_data["path"]):
                check_path = create_folders(
                    candidate.id,
                    candidate.surname,
                    candidate.firstname,
                    candidate.patronymic,
                    "robot",
                )
                try:
                    for item in os.listdir(robot_path):
                        if os.path.isfile(os.path.join(robot_path, item)):
                            shutil.copyfile(item, check_path)
                        elif os.path.isdir(os.path.join(robot_path, item)):
                            shutil.copytree(item, os.path.join(check_path, item))
                except FileNotFoundError as e:
                    db.session.add(Message(report=f"{e}", user_id=user_id))

            db.session.add(Robot(**json_data | {"person_id": candidate.id}))
            db.session.add(
                Message(
                    report=f"Автоматическая проверка {candidate.surname} окончена",
                    user_id=user_id,
                )
            )
            candidate.status_id = Status().get_id(Statuses.reply.value)

        else:
            db.session.add(
                Message(
                    report=f"Результат проверки {candidate.surname} не может быть записан."
                    f"Материал проверки находится в {robot_path}",
                    user_id=user_id,
                )
            )
        db.session.commit()
        return "", 201

bp.add_url_rule("/<item>/<int:item_id>", view_func=ItemsView.as_view("items"))


class FileView(MethodView):

    decorators = [roles_required(Roles.user.value), bp.doc(hide=True)]

    def get(self, item_id):
        """
        Retrieves a file from the server and sends it as a response.
        """
        person = db.session.get(Person, item_id)
        if person.path:
            file_path = os.path.join(
                Config.BASE_PATH, person.path, "image", "image.jpg"
            )
            if os.path.isfile(file_path):
                return send_file(file_path, as_attachment=True)
        return abort(404)

    def post(self, action, item_id=None):
        if not request.files["file"].filename:
            return abort(400)

        if action == "anketa":
            file = request.files["file"]
            filename = secure_filename(file.filename)
            temp_path = os.path.join(
                Config.BASE_PATH,
                f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}\
                                        -{filename}',
            )
            file.save(temp_path)
            anketa = parse_json(temp_path)
            person_id = ResumeView.add_resume(anketa["resume"], "create")
            self.fill_items(anketa, person_id)

            person = db.session.get(Person, person_id)
            if person.path:
                full_path = os.path.join(Config.BASE_PATH, person.path)
                if not os.path.isdir(full_path):
                    os.mkdir(full_path)
            else:
                person.path = os.path.join(
                    person.surname[0].upper(),
                    f"{person_id}-{person.surname} {person.firstname} {person.patronymic}",
                )
                url = os.path.join(Config.BASE_PATH, person.path)
                if not os.path.isdir(url):
                    os.mkdir(url)
            db.session.commit()

            action_folder = create_folders(
                person_id, person.surname, person.firstname, person.patronymic, action
            )

            save_path = os.path.join(Config.BASE_PATH, action_folder, filename)
            if not os.path.isfile(save_path):
                try:
                    shutil.move(temp_path, save_path)
                except Exception as e:
                    print(e)
            return {"message": person_id}

        else:
            files = request.files.getlist("file")
            person = db.session.get(Person, item_id)
            folder = create_folders(
                item_id, person.surname, person.firstname, person.patronymic, action
            )
            if action == "image":
                im = Image.open(files[0])
                rgb_im = im.convert("RGB")
                image_path = os.path.join(folder, "image", "image.jpg")
                if os.path.isfile(image_path):
                    os.remove(image_path)
                rgb_im.save(image_path)
                person.path = folder
                db.session.commit()
            else:
                for file in files:
                    filename = secure_filename(file.filename)
                    for file in files:
                        file.save(
                            os.path.join(
                                Config.BASE_PATH,
                                folder,
                                f'{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}-{filename}',
                            )
                        )
            return "", 201

    def fill_items(self, anketa, person_id):
        models = [Staff, Document, Address, Contact, Workplace, Affilation]
        items_lists = [
            anketa["staff"],
            anketa["passport"],
            anketa["addresses"],
            anketa["contacts"],
            anketa["workplaces"],
            anketa["affilation"],
        ]
        for model, items in zip(models, items_lists):
            for item in items:
                if item:
                    db.session.add(model(**item | {"person_id": person_id}))
        db.session.commit()


file_view = FileView.as_view("file")
bp.add_url_rule("/file/<action>/<int:item_id>", view_func=file_view, methods=["POST"])
