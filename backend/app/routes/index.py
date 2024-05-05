import json
import os

from flask import request, send_file, abort
from flask.views import MethodView
from flask_jwt_extended import current_user
from sqlalchemy_searchable import search
from sqlalchemy import func, select
from PIL import Image

from . import bp
from config import Config
from ..utils.folders import Folders
from ..utils.parsers import Anketa
from .login import roles_required
from ..models.classes import Roles, Statuses
from ..models.model import (
    db,
    Person,
    Check,
    Conclusion,
    Role,
    Status,
    Region,
    User,
    Connect,
)
from ..models.schema import (
    InfoSchema,
    PersonSchema,
    ConclusionSchema,
    RoleSchema,
    StatusSchema,
    RegionSchema,
    UserSchema,
    ConnectSchema,
    AnketaSchemaApi,
)


class IndexView(MethodView):

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
    def get(self, flag, page):
        query = (
            select(Person)
            if current_user.region_id == 1
            else select(Person).filter_by(region_id=current_user.region_id)
        )
        sort_attribute = getattr(Person, request.args.get("sort"))
        if request.args.get("order") == "asc":
            query = query.order_by(sort_attribute.asc())
        else:
            query = query.order_by(sort_attribute.desc())
        if flag == "officer":
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
            search_data = request.args.get("search")
            if search_data:
                query = search(query, "%{}%".format(search_data))

        result = db.paginate(query, page=page, per_page=16, error_out=False)
        return [
            PersonSchema().dump(result, many=True),
            {"has_next": bool(result.has_next), "has_prev": bool(result.has_prev)},
        ]


bp.add_url_rule("/index/<flag>/<int:page>", view_func=IndexView.as_view("index"))


class InformationView(MethodView):

    @roles_required(Roles.user.value)
    @bp.doc(hide=True)
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


bp.add_url_rule("/information", view_func=InformationView.as_view("information"))


class ConnnectView(MethodView):

    decorators = [roles_required(Roles.user.value), bp.doc(hide=True)]

    def get(self, page):
        """
        Retrieves a paginated list of Connect objects based on the specified group and item.
        """
        names = db.session.execute(select(Connect.name)).scalars()
        companies = db.session.execute(select(Connect.company)).scalars()
        cities = db.session.execute(select(Connect.city)).scalars()
        search_data = request.args.get("search")
        query = select(Connect).order_by(Connect.id.desc())
        if search_data:
            query = search(query, "%{}%".format(search_data))
        result = db.paginate(
            query, page=page, per_page=Config.PAGINATION, error_out=False
        )
        return [
            ConnectSchema().dump(result, many=True),
            {"has_prev": result.has_prev},
            {"has_next": result.has_next},
            {"names": list({name for name in names})},
            {"companies": list({company for company in companies})},
            {"cities": list({city for city in cities})},
        ], 200

    @bp.input(ConnectSchema)
    def post(self, json_data):
        """
        Create a new connection.
        """
        db.session.add(Connect(**json_data))
        db.session.commit()
        return {"message": "Created"}, 201

    @bp.input(ConnectSchema)
    def patch(self, item_id, json_data):
        """
        Patch an item in the Connect table.
        """
        resp = db.session.get(Connect, item_id)
        for k, v in json_data.items():
            setattr(resp, k, v)
        db.session.commit()
        return {"message": "Updated"}, 201

    def delete(self, item_id):
        """
        Deletes an item from the database.
        """
        resp = db.session.get(Connect, item_id)
        db.session.delete(resp)
        db.session.commit()
        return {"message": "Deleted"}, 204


contacts_view = ConnnectView.as_view("connect")
bp.add_url_rule("/connect/<int:page>", view_func=contacts_view, methods=["GET"])
bp.add_url_rule("/connect", view_func=contacts_view, methods=["POST"])
bp.add_url_rule(
    "/connect/<int:item_id>",
    view_func=contacts_view,
    methods=["PATCH", "DELETE"],
)


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
        file = request.files["file"]
        if not file.filename:
            return abort(400)

        if action == "anketa":
            json_data = json.load(file)
            json_dict = AnketaSchemaApi().dump(json_data)
            anketa = Anketa(json_dict)
            person_id = anketa.parse_anketa()
            return {"message": person_id}, 201

        person = db.session.get(Person, item_id)
        folders = Folders(
            person.id, person.surname, person.firstname, person.patronymic
        )
        if action == "image":
            folder = folders.create_parent_folder("image")
            im = Image.open(file)
            rgb_im = im.convert("RGB")
            image_path = os.path.join(folder, "image.jpg")
            if os.path.isfile(image_path):
                os.remove(image_path)
            rgb_im.save(image_path)
            return "", 201

        folder = folders.create_subfolder(action)
        files = request.files.getlist("file")
        for file in files:
            if file.filename:
                if not os.path.isfile(os.path.join(folder, file.filename)):
                    file.save(os.path.join(folder, file.filename))
        return "", 201


file_view = FileView.as_view("file")
bp.add_url_rule("/file/<action>/<int:item_id>", view_func=file_view, methods=["POST"])


@roles_required(Roles.user.value)
@bp.route("/image/<int:item_id>")
@bp.doc(hide=True)
def get_image(item_id):
    """
    Retrieves a file from the server and sends it as a response.
    """
    person = db.session.get(Person, item_id)
    folders = Folders(person.id, person.surname, person.firstname, person.patronymic)
    file_path = os.path.join(folders.create_main_folder(), "image", "image.jpg")
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True, mimetype="image/jpg")
    return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")


@bp.get("/classes")
@bp.doc(hide=True)
def get_classes():
    models = [Conclusion, Role, Status, Region, User]
    schemas = [
        ConclusionSchema(),
        RoleSchema(),
        StatusSchema(),
        RegionSchema(),
        UserSchema(),
    ]
    queries = [db.session.execute(select(model)).scalars().all() for model in models]
    dumps = [schema.dump(query, many=True) for query, schema in zip(queries, schemas)]
    return [
        dict(
            (
                d["id"],
                d.get("conclusion")
                or d.get("role")
                or d.get("status")
                or d.get("region")
                or d.get("fullname"),
            )
            for d in sublist
        )
        for sublist in dumps
    ]


@roles_required(Roles.user.value)
@bp.post("/gpt")
@bp.doc(hide=True)
def post_gpt():
    response = request.args.get("query")
    print(response)
    return {
        "answer": "К сожалению, ничего не удалось сгенерировать или сервис отключен"
    }, 201
