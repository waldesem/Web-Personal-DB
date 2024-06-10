from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView

from . import bp
from ..tools.classes import Statuses, Relations
from ..tools.depends import current_user, jwt_required, user_required
from ..tools.parsers import Resume
from ..tools.queries import execute, select_all, select_single


class AnketaView(MethodView):
    @user_required()
    def get(self, person_id):
        action = request.args.get("action")
        upd_query = "UPDATE persons SET status = ? user_id = ? WHERE id = ?"
        if action == "status":
            execute(
                upd_query,
                (
                    Statuses.update.name,
                    None,
                    person_id,
                ),
            )
        if action == "self":
            execute(
                upd_query,
                (
                    Statuses.manual.name,
                    current_user["id"],
                    person_id,
                ),
            )
        person = select_single(
            "SELECT * FROM persons WHERE id = ?",
            (person_id,),
        )
        if person["user_id"]:
            user_fullname = select_single(
                "SELECT fullname FROM users WHERE id = ?", (person["user_id"],)
            )
            person["username"] = user_fullname["fullname"]
        return jsonify(person), 200

    @jwt_required()
    def delete(self, person_id):
        execute("DELETE FROM persons WHERE id = ?", (person_id,))
        return "", 204

    @user_required()
    def patch(self, person_id):
        json_data = request.get_json()
        resume = Resume(json_data)
        resume.update_resume(person_id, manual=True)
        return jsonify({"message": person_id}), 201

    @user_required()
    def post(self):
        json_data = request.get_json()
        resume = Resume(json_data)
        person_id = resume.update_status()
        return jsonify({"message": person_id}), 201


resume_view = AnketaView.as_view("resume")
bp.add_url_rule(
    "/resume",
    view_func=resume_view,
    methods=["POST"],
)
bp.add_url_rule(
    "/resume/<int:person_id>",
    view_func=resume_view,
    methods=["GET", "DELETE", "PATCH"],
)


class RelationView(MethodView):
    @jwt_required()
    def post(self, item_id):
        json_data = request.get_json()
        execute(
            "INSERT INTO relations (relation, relation_id) VALUES(?, ?, ?)",
            [
                (
                    json_data["relation"],
                    json_data["relation_id"],
                    item_id,
                ),
                (
                    json_data["relation"],
                    item_id,
                    json_data["relation_id"],
                ),
            ],
        )
        return "", 201


prev_view = RelationView.as_view("relations")
bp.add_url_rule("/relations/<int:item_id>", view_func=prev_view, methods=["POST"])


class PreviousView(MethodView):
    @jwt_required()
    def post(self, item_id):
        json_data = request.get_json()
        person = select_single("SELECT * FROM persons WHERE id = ?", (item_id,))
        exist = Resume.get_person(
            person["surname"].strip().upper(),
            person["firstname"].strip().upper(),
            person.get("patronymic").strip().upper()
            if person.get("patronymic")
            else "",
            datetime.strptime(person["birthday"], "%Y-%m-%d").date(),
        )
        if exist:
            execute(
                "INSERT INTO relations (relation, relation_id, person_id) VALUES (?, ?, ?)",
                [
                    (
                        Relations.similar.name,
                        exist["id"],
                        item_id,
                    ),
                    (
                        Relations.similar.name,
                        item_id,
                        exist["id"],
                    ),
                ]
            )
        cols = ",".join(json_data.keys())
        vals = ",".join(["?" for _ in cols])
        execute(
            "INSERT INTO previous ({}) VALUES ({})".format(cols, vals),
            (tuple(json_data.values())),
        )
        return "", 201


prev_view = PreviousView.as_view("previous")
bp.add_url_rule("/previous/<int:item_id>", view_func=prev_view, methods=["POST"])


class ItemsView(MethodView):
    @jwt_required()
    def get(self, item, item_id):
        results = select_all(
            f"SELECT * FROM {item} WHERE person_id = ? ORDER BY id ASC",
            (item_id,),
        )
        if item in ["checks", "poligrafs", "inquiries", "investigations"]:
            users = select_all("SELECT id, fullname FROM users")
            names = {user["id"]: user["fullname"] for user in users}
            for res in results:
                if "user_id" in res:
                    res["user"] = names[res["user_id"]]
        return jsonify(results)

    @jwt_required()
    def delete(self, item, item_id):
        execute(
            f"DELETE FROM {item} WHERE id = ?",
            (item_id,),
        )
        return "", 204

    @user_required()
    def post(self, item, item_id):
        json_data = request.get_json() | {"person_id": str(item_id)}
        json_dict = {}
        for k, v in json_data.items():
            if k in ["issue", "start_date", "end_date"]:
                json_dict[k] = datetime.strptime(v, "%Y-%m-%d").date() if v else None
            elif k in ["now_work", "pfo"]:
                json_dict[k] = True if v else False
            else:
                json_dict[k] = v
        if item in ["checks", "poligrafs", "inquiries", "investigations"]:
            json_dict["user_id"] = str(current_user["id"])
        cols = ",".join(json_dict.keys())
        vals = ",".join("?" for _ in cols)
        execute(
            f"INSERT INTO {item} ({cols}) VALUES ({vals})",
            (tuple(json_dict.values())),
        )
        if item == "checks":
            args = []
            if json_data.get("pfo"):
                args.extend([Statuses.poligraf.name, "", item_id])
            else:
                args.extend([Statuses.finish.name, "", item_id])
            execute(
                "UPDATE persons SET status = ? user_id = ? WHERE id = ?", tuple(args)
            )
        if item == "poligrafs":
            person = select_single(
                "SELECT status FROM persons WHERE id = ?", (item_id,)
            )
            if person["status"] == Statuses.poligraf.name:
                args = (
                    Statuses.finish.name,
                    "",
                    item_id,
                )
                execute("UPDATE persons SET status = ? user_id = ? WHERE id = ?", args)
        return "", 201

    @user_required()
    def patch(self, item, item_id):
        json_data = request.get_json()
        json_dict = {}
        for k, v in json_data.items():
            if k not in ["updated", "created", "username"]:
                if k in ["issue", "start_date", "end_date"]:
                    json_dict[k] = datetime.strptime(v, "%Y-%m-%d").date()
                elif k in ["now_work", "pfo"]:
                    json_dict[k] = bool(v) if v else False
                elif k == "user_id":
                    json_dict[k] = current_user["id"]
                else:
                    json_dict[k] = v
        query = "UPDATE persons SET "
        args = []
        if item in ["inquiries", "investigations"]:
            query += " updated = ? "
            args.append(datetime.now())
        query += {",".join([key + "=?" for key in json_dict.keys()])}
        args.extend(json_dict.values())
        execute(query + " WHERE person_id = ?", tuple(args + [item_id]))
        return "", 201


items_view = ItemsView.as_view("items")
bp.add_url_rule(
    "/<item>/<int:item_id>", view_func=items_view, methods=["GET", "DELETE"]
)
