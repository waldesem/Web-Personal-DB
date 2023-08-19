import shutil
import os
import re

import bcrypt
from apiflask import HTTPBasicAuth

from ..routes import bp
from ..routes.route import add_resume, folder_check
from ..utils.excel import resume_data
from ..models.model import db, User, Person, Region, Check, Report, Status
from ..models.schema import CheckSchemaApi, PersonSchemaApi
from ..models.classify import Role

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str):
    """
    Verify the password for a given username.
    Args:
        username (str): The username to verify.
        password (str): The password to verify.
    Returns:
        str: An empty string if the password is verified, otherwise None.
    """
    user = db.session.query(User).filter_by(username=username).one_or_none()
    if user and not user.blocked and user.has_role(Role.api.value):
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return ''


@bp.post('/api/v1/anketa')
@bp.input(PersonSchemaApi)
@bp.auth_required(auth)
def get_anketa(json_data):
    """
    Take a new anketa.
    Parameters:
        anketa (dict): The anketa data as a dictionary.
    Returns:
        Tuple[bool, int]: A tuple containing a boolean indicating the success of 
        the operation and an HTTP status code.
    """
    resume = json_data['resume']
    resume["request_id"] = resume.pop('id')
    regions = {rgn[1]: rgn[0] for rgn in db.session.query(Region.id, Region.region).all()}
    division = re.split(r'/', json_data['staff']['department'])
    location_id = 1
    for div in division:
        location_id = regions[div] if div.strip() in regions else 1  # Проверка на существование региона и запись id, если нет - 'Главный офис'
            
            
    person_id, result = add_resume(resume, location_id)
        
    users = db.session.query(User).filter(User.role.in_(['superuser', 'user']), 
                                                        User.region_id == location_id).all()
    for user in users:
        db.session.add(Report(report=f'Поступила анкета {resume["fullname"]}', 
                               user_id=user.id))
    db.session.commit()

    resume_data(person_id, json_data['document'], json_data['addresses'], 
                json_data['contacts'], json_data['workplaces'], json_data['staff'])
    return '', 200


@bp.post('/api/v1/check')
@bp.input(CheckSchemaApi)
@bp.auth_required(auth)
def check_in(json_data):
    """
    Take a new check result candidate.
    Parameters:
    - response: A dictionary containing the response data from the client.
    Returns:
    - An empty string and a status code of 200 indicating a successful check-in.
    """
    candidate = db.session.query(Person).get(json_data['id'])
    del json_data['id']
    latest_check = db.session.query(Check).filter_by(person_id=candidate.id).order_by(Check.id.desc()).first()
    user = db.session.query(User).filter_by(username=latest_check.officer).one_or_none().scalar()
    
    db.session.add(Report(message=f'Проверка кандидата {candidate.fullname} окончена', user_id=user.id))

    if os.path.isdir(json_data['path']):
        check_path = latest_check.path if os.path.isdir(latest_check.path) else folder_check(candidate.id, candidate["fullname"])
        try:
            for file in os.listdir(json_data['path']):
                shutil.copyfile(file, check_path)
        except FileNotFoundError as error:
            db.session.add(Report(message=error, user_id=user.id))
    
    for k, v in json_data.items():
        setattr(latest_check, k, v)
    
    candidate.status = Status.reply.value
    db.session.commit()
    
    return '', 200

