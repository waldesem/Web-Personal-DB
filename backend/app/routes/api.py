import shutil
import os
import re

import bcrypt
from apiflask import HTTPBasicAuth

from . import bp
from .. import db
from ..utils.utilities import add_resume, create_folders
from ..models.model import Staff, Document, Contact, Workplace,Address,\
      User, Person, Region, Check, Report, Status
from ..models.schema import CheckSchemaApi, AnketaSchemaApi
from ..models.classes import Roles

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
    if user and not user.blocked and user.has_role(Roles.api.value):
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return ''


@bp.post('/api/v1/anketa')
@bp.auth_required(auth)
@bp.input(AnketaSchemaApi)
def anketa_in(json_data):
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
    regions = {rgn[1]: rgn[0] for rgn in db.session.query(Region.id, 
                                                          Region.region).all()}
    
    division = re.split(r'/', json_data['staff'][0]['department'])
    location_id = [regions.get(key.strip(), 1) for key in division][0]
                  
    person_id = add_resume(resume, location_id, 'api')
    
    models = [Staff, Document, Address, Contact, Workplace]
    for count, items in enumerate([json_data['staff'], json_data['document'], 
                                   json_data['addresses'],json_data['contacts'], 
                                   json_data['workplaces']]):
        for item in items:
            if item:
                db.session.add(models[count](**item | {'person_id': person_id}))

    users = db.session.query(User).filter_by(region_id=location_id).all()
    for user in users:
        if user:
            db.session.add(Report(report=f'Поступила анкета #{person_id} {resume["fullname"]}',
                                  user_id=user.id))
    db.session.commit()
    return '', 201


@bp.post('/api/v1/check')
@bp.auth_required(auth)
@bp.input(CheckSchemaApi)
def check_in(json_data):
    """
    Take a new check result candidate.
    Parameters:
    - response: A dictionary containing the response data from the client.
    Returns:
    - An empty string and a status code of 201 indicating a successful check-in.
    """
    candidate = db.session.query(Person).get(json_data['id'])
    del json_data['id']
    latest_check = db.session.query(Check).filter_by(person_id=candidate.id).\
        order_by(Check.id.desc()).first()
    user = db.session.query(User).filter_by(fullname=latest_check.officer).one_or_none()
    
    if candidate.status == Status.robot.value:
        if os.path.isdir(json_data['path']):
            check_path = latest_check.path if os.path.isdir(latest_check.path) \
                else create_folders(candidate.id, candidate["fullname"])
            try:
                for file in os.listdir(json_data['path']):
                    shutil.copyfile(file, check_path)
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
