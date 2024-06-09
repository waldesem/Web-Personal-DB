from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView

from . import bp
from ..tools.depends import current_user, jwt_required, user_required
from ..tools.parsers import Resume
from ..tools.queries import execute, select_all, select_single
from ..tools.classes import Statuses, Conclusions


class AnketaView(MethodView):
    @user_required()
    def get(self, person_id):
        action = request.args.get("action")
        if action == "status":
            execute(
                "UPDATE persons SET status = ? user_id = ? WHERE id = ?",
                (
                    Statuses.update.name,
                    None,
                    person_id,
                ),
            )
        if action == "self":
            execute(
                "UPDATE persons SET status = ? user_id = ? WHERE id = ?",
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


class ItemsView(MethodView):

    @staticmethod
    def post_patch_checks(json_data, item_id):
        if json_data["conclusion"] == Conclusions.saved.name:
            execute(
                "UPDATE persons SET status = ? WHERE id = ?",
                (
                    Statuses.save.name,
                    item_id,
                ),
            )
        else:
            if json_data.get("pfo"):
                execute(
                    "UPDATE persons SET status = ? user_id = ? WHERE id = ?",
                    (Statuses.poligraf.name, "", item_id,),
                )
            else:
                execute(
                    "UPDATE persons SET status = ? user_id = ? WHERE id = ?",
                    (Statuses.finish.name, "", item_id,),
                )

    @jwt_required()
    def get(self, item, item_id):
        items = select_all(
            f"SELECT * FROM {item} WHERE person_id = ? ORDER BY id ASC",
            (item_id,),
        )
        if item in ["checks", "poligrafs", "inquiries", "investigations"]:
            users = select_all("SELECT id, fullname FROM users")
            names = {u["id"]: u["fullname"] for u in users}
            for i in items:
                if i["user_id"]:
                    i["user"] = names[i["user_id"]]
        return jsonify(items)

    @user_required()
    def post(self, item, item_id):
        json_data = request.get_json() | {"person_id": str(item_id)}
        for k, v in json_data.items():
            if k in ["issue", "start_date", "end_date"]:
                json_data[k] = datetime.strptime(v, "%Y-%m-%d").date() if v else None
            elif k in ["now_work", "pfo"]:
                json_data[k] = True if v else False

        person = select_single("SELECT * FROM persons WHERE id = ?", (item_id,))
        if item == "previous":
            prev = select_single(
                "SELECT * FROM persons \
                WHERE surname LIKE '%{}%' AND firstname LIKE '%{}%' AND patronymic LIKE '%{}%' AND birthday = ?".format(
                    person["surname"].strip().upper(),
                    person["firstname"].strip().upper(),
                    person.get("patronymic").strip().upper()
                    if person.get("patronymic")
                    else "",
                ),
                (datetime.strptime(person["birthday"], "%Y-%m-%d"),),
            )
            if prev:
                execute(
                    "INSERT INTO relations (relation, person_id, relation_id) VALUES(?, ?, ?)",
                    (
                        "Одно лицо",
                        prev["id"],
                        item_id,
                    ),
                )

        if item == "relations":
            execute(
                "INSERT INTO relations (relation, person_id, relation_id) VALUES(?, ?, ?)",
                (
                    json_data["relation"],
                    item_id,
                    json_data["relation_id"],
                ),
            )

        if item in ["checks", "poligrafs", "inquiries", "investigations"]:
            json_data["user_id"] = str(current_user["id"])
            if item == "checks":
                self.post_patch_checks(json_data, item_id)

            if item == "poligrafs":
                if person["status"] == Statuses.poligraf.name:
                    execute(
                        "UPDATE persons SET status = ? WHERE id = ?",
                        (Statuses.finish.name, item_id),
                    )
        cols = ",".join(json_data.keys())
        execute(
            f"INSERT INTO {item} ({cols}) VALUES ({','.join('?' for _ in json_data.keys())})",
                (tuple(json_data.values())),
        )
        return "", 201

    @user_required()
    def patch(self, item, item_id):
        json_data = request.get_json()
        json_dict = {}
        for k, v in json_data.items():
            if k not in ["updated", "username"]:
                if k in ["issue", "start_date", "end_date"]:
                    json_data[k] = datetime.strptime(v, "%Y-%m-%d").date()
                elif k == "created":
                    json_data[k] = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
                elif k in ["now_work", "pfo"]:
                    json_data[k] = bool(v) if v else False
                elif k == "user_id":
                    json_data[k] = current_user["id"]
                else:
                    json_dict[k] = v
        query = "UPDATE persons SET "
        args = []
        if item in ["checks", "poligrafs", "inquiries", "investigations"]:
            if item == "checks":
                self.post_patch_checks(json_data, item_id)
            query += "updated = ? "
            args.append(datetime.now())
        query += f"{','.join([key + '=?' for key in json_data.keys()])} WHERE person_id = ?"
        args.extend(json_data.values())
        execute(query, tuple(args))
        return "", 201

    @jwt_required()
    def delete(self, item, item_id):
        execute(
            f"DELETE FROM {item} WHERE id = ?",
            (item_id,),
        )
        return "", 204


bp.add_url_rule("/<item>/<int:item_id>", view_func=ItemsView.as_view("items"))
