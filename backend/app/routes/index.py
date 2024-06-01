import json
import os

from flask import jsonify, request, send_file, abort
from flask.views import MethodView
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from PIL import Image

from . import bp
from config import Config
from ..utils.folders import Folders
from ..utils.parsers import Anketa
from ..utils.dependencies import Token, roles_required
from ..models.classes import Roles, Statuses
from ..models.model import (
    engine,
    Person,
    Check,
    Conclusion,
    Role,
    Status,
    Region,
    User,
    Connect,
)


class IndexView(MethodView):

    @roles_required(Roles.user.value)
    def get(self, flag, page):
        query = (
            select(Person)
            if Token.current_user.region_id == 1
            else select(Person).filter_by(region_id=Token.current_user.region_id)
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
                Person.user_id == Token.current_user.id,
            )
        else:
            search_data = request.args.get("search")
            if search_data:
                query = query.filter_by(surname="%{}%".format(search_data))
        with Session(engine) as session:
            pagination = query.offset((page - 1) * Config.PAGINATION).limit(
                Config.PAGINATION + 1
            )
            result = session.execute(pagination).all()
            has_next = True if len(result) > Config.PAGINATION else False
            return {
                "persons": result if not has_next else result[:-1],
                "has_next": has_next,
                "has_prev": True if page > 1 else False
            }


bp.add_url_rule("/index/<flag>/<int:page>", view_func=IndexView.as_view("index"))


class InformationView(MethodView):

    @roles_required(Roles.user.value)
    def get_information(query_data):
        query_data = request.args
        with Session(engine) as session:
            candidates = session.execute(
                select(Check.conclusion_id, func.count(Check.id))
                .join(Person)
                .group_by(Check.conclusion_id)
                .filter(Person.region_id == query_data["region_id"])
                .filter(Check.deadline.between(query_data["start"], query_data["end"]))
            ).all()
            return jsonify(dict(map(lambda x: (x[1], x[0]), candidates)))


bp.add_url_rule("/information", view_func=InformationView.as_view("information"))


class ConnnectView(MethodView):

    decorators = [roles_required(Roles.user.value)]

    def get(self, page):
        """
        Retrieves a paginated list of Connect objects based on the specified group and item.
        """
        with Session(engine) as session:
            search_data = request.args.get("search")
            query = select(Connect).order_by(Connect.id.desc())
            if search_data:
                query = query.filter_by(company="%{}%".format(search_data))
                pagination = query.offset((page - 1) * Config.PAGINATION).limit(
                    Config.PAGINATION + 1
                )
            result = session.execute(pagination).all()
            has_next = True if len(result) > Config.PAGINATION else False
            return {
                "contacts": result if not has_next else result[:-1],
                "has_next": has_next,
                "has_prev": True if page > 1 else False,
                "names": [name for name in session.exec(select(Connect.name)).all()],
                "companies": [
                    company for company in session.exec(select(Connect.company)).all()
                ],
                "cities": [city for city in session.exec(select(Connect.city)).all()],
            }

    def post(self):
        """
        Create a new connection.
        """
        json_data = request.get_json()
        with Session(engine) as session:
            session.add(Connect(**json_data))
            session.commit()
            return {"message": "Created"}

    def patch(self, item_id, json_data):
        """
        Patch an item in the Connect table.
        """
        json_data = request.get_json()
        with Session(engine) as session:
            resp = session.get(Connect, item_id)
            for k, v in json_data.items():
                setattr(resp, k, v)
            session.commit()
            return {"message": "Updated"}

    def delete(self, item_id):
        """
        Deletes an item from the database.
        """
        with Session(engine) as session:
            resp = session.get(Connect, item_id)
            session.delete(resp)
            session.commit()
            return {"message": "Deleted"}


contacts_view = ConnnectView.as_view("connect")
bp.add_url_rule("/connect/<int:page>", view_func=contacts_view, methods=["GET"])
bp.add_url_rule("/connect", view_func=contacts_view, methods=["POST"])
bp.add_url_rule(
    "/connect/<int:item_id>",
    view_func=contacts_view,
    methods=["PATCH", "DELETE"],
)


class FileView(MethodView):

    decorators = [roles_required(Roles.user.value)]

    def get(self, item_id):
        """
        Retrieves a file from the server and sends it as a response.
        """
        with Session(engine) as session:
            person = session.get(Person, item_id)
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
            json_dict = json.load(file)
            anketa = Anketa(json_dict)
            person_id = anketa.parse_anketa()
            return {"message": person_id}
        
        with Session(engine) as session:
            person = session.get(Person, item_id)
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
                return ""

            folder = folders.create_subfolder(action)
            files = request.files.getlist("file")
            for file in files:
                if file.filename:
                    if not os.path.isfile(os.path.join(folder, file.filename)):
                        file.save(os.path.join(folder, file.filename))
            return ""


file_view = FileView.as_view("file")
bp.add_url_rule("/file/<action>/<int:item_id>", view_func=file_view, methods=["POST"])


@roles_required(Roles.user.value)
@bp.route("/image/<int:item_id>")
def get_image(item_id):
    """
    Retrieves a file from the server and sends it as a response.
    """
    with Session(engine) as session:
        person = session.get(Person, item_id)
        folders = Folders(person.id, person.surname, person.firstname, person.patronymic)
        file_path = os.path.join(folders.create_main_folder(), "image", "image.jpg")
        if os.path.isfile(file_path):
            return send_file(file_path, as_attachment=True, mimetype="image/jpg")
        return send_file("static/no-photo.png", as_attachment=True, mimetype="image/jpg")


@bp.get("/classes")
def get_classes():
    models = [Conclusion, Role, Status, Region, User]
    with Session(engine) as session:
        queries = [session.execute(select(model)).scalars().all() for model in models]
        return [
            dict(
                (
                    d.id,
                    d.conclusion if hasattr(d, "conclusion") \
                        else d.role if hasattr(d, "role") \
                            else d.status if hasattr(d, "status") \
                                else d.region if hasattr(d, "region") \
                                    else d.fullname if hasattr(d, "fullname") \
                                        else None,
                )
                for d in sublist
            )
            for sublist in queries  
        ]


@roles_required(Roles.user.value)
@bp.post("/gpt")
def post_gpt():
    response = request.args.get("query")
    print(response)
    return {
        "answer": "К сожалению, ничего не удалось сгенерировать или сервис отключен"
    }
