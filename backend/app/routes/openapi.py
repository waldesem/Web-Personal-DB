import os
import shutil

from apiflask import EmptySchema
from flask.views import MethodView

from . import bp
from ..utils.folders import Folders
from ..models.schema import  RobotSchema, AnketaSchemaApi
from ..models.model import db, Person, Message, Robot
from ..utils.parsers import Anketa


class RobotsView(MethodView):

    example = {
        "bankruptcy": "Признан банкротом",
        "bki": "Положительная кредитная история",
        "courts": "Есть судебные решения",
        "debt": "Наличие задолженности",
        "employee": "Ранее работал в компании с 2000 по 2010 года",
        "id": 0,
        "inn": "Проверка пройдена",
        "mvd": "Проверка пройдена",
        "path": "/path/to/robot",
        "terrorist": "Проверка пройдена",
    }

    @bp.input(RobotSchema, example=example)
    @bp.output(EmptySchema, status_code=201)
    def post(self, json_data):
        """
        Post method for the given API endpoint.
        """
        robot_path = json_data.pop("path")
        candidate = db.session.get(Person, json_data.pop("id"))

        if not candidate:
            db.session.add(
                Message(
                    message=f"Результат {candidate.surname} не может быть записан."
                    f"Файлы находятся в {robot_path}",
                    user_id=candidate.user_id,
                )
            )
        else:
            if os.path.isdir(robot_path):
                folders = Folders(
                    candidate.id,
                    candidate.surname,
                    candidate.firstname,
                    candidate.patronymic,
                )
                check_path = folders.create_subfolder("robot")
                try:
                    for item in os.listdir(robot_path):
                        item_path = os.path.join(robot_path, item)
                        if os.path.isfile(item_path):
                            shutil.copyfile(item_path, os.path.join(check_path, item))
                        elif os.path.isdir(item_path):
                            shutil.copytree(item_path, os.path.join(check_path, item))
                except FileNotFoundError as e:
                    db.session.add(Message(message=f"{e}", user_id=candidate.user_id))

            db.session.add(Robot(**json_data | {"person_id": candidate.id}))
            db.session.add(
                Message(
                    message=f"Автоматическая проверка {candidate.surname} окончена",
                    user_id=candidate.user_id,
                )
            )
        db.session.commit()
        return ""


bp.add_url_rule("/robot", view_func=RobotsView.as_view("robot"))


class PulseView(MethodView):

    example = {
        "additionalCitizenship": "Беларусь, Израиль",
        "birthday": "2002-12-12",
        "birthplace": "Беларусь, Минск",
        "citizen": "Россия",
        "contactPhone": "+375 29 123 45 67",
        "department": "Департамент тестирования",
        "education": [
            {
            "end": 2021,
            "name": "Институт тестирования",
            "specialty": "тестирование",
            "view": "высшее"
            }
        ],
        "email": "email@bk.ru",
        "experience": [
            {
            "address": "Россия, Москва, ул. Большая Конюшенная, д. 1",
            "end_date": "1999-01-01",
            "now_work": False,
            "position": "тестировщик",
            "reason": "по собственному желанию",
            "start_date": "1998-01-01",
            "workplace": "ООО Тест"
            }
        ],
        "firstName": "Иван",
        "inn": "123456789010",
        "lastName": "Иванов",
        "maritalStatus": "женат",
        "midName": "Иванович",
        "nameWasChanged": [
            {
            "date_change": 2021,
            "firstname": "Семен",
            "patronymic": "Семенович",
            "reason": "по собственному желанию",
            "surname": "Семенов"
            }
        ],
        "organizations": [
            {
            "inn": "123456789010",
            "name": "ООО БелТест",
            "position": "Директор"
            }
        ],
        "passportIssueDate": "2024-01-01",
        "passportIssuedBy": "МВД России",
        "passportNumber": "1234",
        "passportSerial": "123654",
        "positionName": "тестировщик",
        "publicOfficeOrganizations": [
            {
            "name": "МИД России",
            "position": "тестировщик"
            }
        ],
        "regAddress": "Россия, Москва, ул. Тестовая, д. 1",
        "relatedPersonsOrganizations": [
            {
            "name": "ЦБ России",
            "position": "Директор Департамента тестирования",
            }
        ],
        "snils": "12345678901",
        "stateOrganizations": [
            {
            "name": "ФСПП России",
            "position": "пристав"
            }
        ],
        "validAddress": "Россия, Москва, ул. Тестовая, д. 1",
        }
    
    @bp.input(AnketaSchemaApi, location="json", example=example)
    @bp.output(EmptySchema, status_code=201)
    def post(self, json_data):
        """
        Post method for the given API endpoint.
        """
        anketa = Anketa(json_data)
        anketa.parse_anketa()

        return ""
    
bp.add_url_rule("/pulse", view_func=PulseView.as_view("pulse"))
