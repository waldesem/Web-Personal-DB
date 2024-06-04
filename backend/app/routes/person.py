from datetime import datetime
import sqlite3

from flask import jsonify, request, abort
from flask.views import MethodView

from config import Config
from . import bp
from ..utils.dependencies import Token, roles_required
from ..utils.parsers import Resume, Anketa
from ..models.classes import Roles, Statuses, Conclusions


class AnketaView(MethodView):
    decorators = [roles_required(Roles.user.value)]

    def get(self, person_id):
        action = request.args.get("action")
        person = ResumeAction(person_id)
        if action == "status":
            person.change_status(Statuses.update.value)
            return {"message": action}, 201
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            if action == "self" and not person.anketa["user_id"]:
                cursor.execute(
                    "INSERT INTO messages (message, user_id) VALUES (?, ?)",
                    (
                        f"Aнкета ID #{person_id} принята в работу",
                        Token.current_user["id"],
                    ),
                )
                conn.commit()
                person.change_status(Statuses.manual.value, Token.current_user["id"])
                return {"message": action}, 201
        return jsonify({"message": person.anketa})

    def delete(self, person_id):
        person = ResumeAction(person_id)
        person.del_person()
        return "", 204

    def patch(self, person_id):
        json_data = request.get_json()
        resume = Resume(json_data)
        resume.update_resume(person_id)
        return jsonify({"message": person_id}), 201

    def post(self):
        json_data = request.get_json()
        resume = Resume(json_data)
        person_id = resume.check_resume()
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


class ResumeAction:
    def __init__(self, person_id):
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query = cursor.execute(
                "SELECT * FROM persons WHERE id = ?", 
                (person_id,)
            )
            self.anketa = query.fetchone()

    def change_status(self, status, user_id=None):
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE persons SET status_id = ? user_id = ? WHERE id = ?",
                (status, self.anketa["id"], user_id),
            )
            conn.commit()

    def del_person(self):
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM persons WHERE id = ?", 
                (self.anketa["id"],)
            )
            conn.commit()


class ItemsView(MethodView):
    decorators = [roles_required(Roles.user.value)]

    @staticmethod
    def select_status_id(status):
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query_status = cursor.execute(
                "SELECT id FROM statuses WHERE status = ?",
                (status,),
            )
            return query_status.fetchone()[0]

    def get(self, item, item_id):
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query = cursor.execute(
                "SELECT * FROM {} WHERE person_id = ? ORDER BY id DESC".format(item),
                (item_id,),
            )
            col_names = [i[0] for i in query.description]
            results = [zip(col_names, q) for q in query.fetchall()]
            if not results:
                abort(404)
            return jsonify(results)

    def post(self, item, item_id):
        response = request.get_json() | {"person_id": item_id}
        json_data = {}
        for k, v in response.items():
            if k in [
                "birthday",
                "date_change",
                "issue",
                "start_date",
                "end_date",
                "deadline",
            ]:
                json_data.update(
                    {k: datetime.strptime(v, "%Y-%m-%d").date()}
                ) if v else None
            elif k in ["now_work", "pfo"]:
                json_data.update({k: bool(v)}) if v else False
            else:
                json_data.update({k: v})
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            query_person = cursor.execute(
                "SELECT * FROM persons WHERE id = ?", (item_id,)
            )
            person = query_person.fetchone()
            if item == "previous":
                query_prev = cursor.execute(
                    "SELECT * FROM persons WHERE "
                    "surname = ? AND firstname = ? AND patronymic = ? AND birthday = ?",
                    (
                        person["surname"].upper(),
                        person["firstname"].upper(),
                        person.get("patronymic").upper()
                        if person.get("patronymic")
                        else None,
                        person["birthday"],
                    ),
                )
                col_names = [i[0] for i in query_prev.description]
                prev = zip(col_names, query_prev.fetchone())
                if prev:
                    cursor.execute(
                        "INSERT INTO messages (message, user_id) VALUES (?, ?)",
                        (
                            f"Кандидат ранее проверялся ID: {prev['id']}",
                            Token.current_user["id"],
                        ),
                    )
                    conn.commit()
                    Anketa.add_relation("Одно лицо", prev["id"], item_id)

            if item == "relation":
                Anketa.add_relation(
                    json_data["relation"], item_id, json_data["relation_id"]
                )

            if item in ["check", "poligraf", "inquiry", "investigation"]:
                json_data = json_data | {"user_id": Token.current_user.id}
                if item == "check":
                    query_conclusion = cursor.execute(
                        "SELECT id FROM conclusions WHERE conclusion = ?",
                        (Conclusions.saved.value,),
                    )
                    conclusion_id = query_conclusion.fetchone()[0]
                    save_id = self.select_status_id(Statuses.save.value)
                    if json_data["conclusion_id"] == conclusion_id:
                        cursor.execute(
                            "UPDATE persons SET status_id = ? WHERE id = ?",
                            (save_id, item_id),
                        )
                    else:
                        if json_data.get("pfo"):
                            pfo_id = self.select_status_id(Statuses.poligraf.value)
                            cursor.execute(
                                "UPDATE persons SET status_id = ? user_id = ? WHERE id = ?",
                                (pfo_id, None, item_id),
                            )
                        else:
                            finish_id = self.select_status_id(Statuses.finish.value)
                            cursor.execute(
                                "UPDATE persons SET status_id = ? user_id = ? WHERE id = ?",
                                (finish_id, None, item_id),
                            )

                if item == "poligraf":
                    pfo_id = self.select_status_id(Statuses.poligraf.value)
                    finish_id = self.select_status_id(Statuses.finish.value)
                    if person["status_id"] == pfo_id:
                        cursor.execute(
                            "UPDATE persons SET status_id = ? WHERE id = ?",
                            (finish_id, item_id),
                        )

            cursor.execute(
                "INSERT INTO {} ({}) VALUES ({})".format(
                    item, ", ".join(json_data.keys()), ", ".join(["?"] * len(json_data))
                ),
            )
            conn.commit()
            return "", 201

    def patch(self, item, item_id):
        json_data = request.get_json()
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            for k, v in json_data.items():
                if k != "deadline":
                    if k in [
                        "birthday",
                        "date_change",
                        "issue",
                        "start_date",
                        "end_date",
                    ]:
                        json_data[k] = datetime.strptime(v, "%Y-%m-%d").date()
                    elif k in ["now_work", "pfo"]:
                        json_data[k] = bool(v) if v else False
            cursor.execute(
                f"UPDATE {item} SET {','.join(key + '=?' for key in json_data.keys())} WHERE person_id = ?",
                tuple(json_data.values()) + (item_id,),
            )
            conn.commit()
            return "", 201

    def delete(self, item, item_id):
        with sqlite3.connect(Config.DATABASE_URI) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {item} WHERE person_id = ?",
                (item_id,),
            )
            conn.commit()
            return "", 204


bp.add_url_rule("/<item>/<int:item_id>", view_func=ItemsView.as_view("items"))
