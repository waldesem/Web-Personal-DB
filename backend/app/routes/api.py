import shutil
import os

import bcrypt
from apiflask import HTTPBasicAuth
from flask import current_app

from . import bp
from .. import db
from ..utils.utilities import create_folders
from ..models.model import User, Person, Check, Report, Status
from ..models.schema import CheckSchemaApi
from ..models.classes import Roles

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str):
    user = db.session.query(User).filter_by(username=username).one_or_none()
    if user and not user.blocked and user.has_role(Roles.api.value):
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return ''

@bp.post('/api/v1/check')
@bp.auth_required(auth)
@bp.input(CheckSchemaApi)
def check_in(json_data):
    candidate = db.session.query(Person).get(json_data['id'])
    del json_data['id']
    latest_check = db.session.query(Check).filter_by(person_id=candidate.id).\
        order_by(Check.id.desc()).first()
    user = db.session.query(User).filter_by(fullname=latest_check.officer).one_or_none()
    
    if candidate.status == Status.robot.value:
        if os.path.isdir(json_data['path']):
            full_path = os.path.join(current_app.config["BASE_PATH"], latest_check.path)
            check_path = full_path if os.path.isdir(full_path) \
                else create_folders(candidate.id, candidate["fullname"], 'check')
            
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
