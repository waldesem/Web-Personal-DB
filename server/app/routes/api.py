from datetime import datetime
import shutil
import os

import bcrypt
from apiflask import HTTPBasicAuth

from ..routes import bp
from ..utils.excel import resume_data
from ..models.model import db, User, Person, Region, Check, Message, Status
from ..models.schema import CheckSchema, ResumeSchema
from ..models.classify import BASE_PATH, Role

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str):
    """
    Verifies the password for a given username.
    Parameters:
        - username (str): The username to verify the password for.
        - password (str): The password to verify.
    Returns:
        - str: The username if the password is verified, else None.
    """
    user = db.session.query(User).filter_by(username=username).one_or_none()
    if user and not user.blocked and user.has_role(Role.api.value):
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return username


@bp.post('/api/v1/anketa')
@bp.input(ResumeSchema)
@bp.auth_required(auth)
def anketa(resume: dict):

    resume['resume']["request_id"] = resume['resume'].pop('id')
    location_id = db.session.query(Region.id).filter_by(region=resume['resume']['region']).one_or_none().scalar()
    resume['resume']['region_id'] = location_id
    candidate = db.session.query(Person).filter(
        Person.fullname.ilike(f"{resume['resume']['fullname']}"),
        Person.birthday == resume['resume']['birthday']
    ).one_or_none()

    if candidate:
        resume['resume']['status'] = Status.update.value
        for k, v in resume['resume'].items():
            setattr(candidate, k, v)
        new_id = candidate.id
        
        if candidate.path and not os.path.isdir(candidate.path):
            os.mkdir(candidate.path)
        else:
            new_path = os.path.join(BASE_PATH, f'{new_id}-{resume["fullname"]}')
            if not os.path.isdir(new_path):
                os.mkdir(new_path)
                setattr(candidate, 'path', new_path)
                db.session.commit()

    else:
        value = Person(**resume['resume'])
        db.session.add(value)
        db.session.flush()
        new_id = value.id
        path = os.path.join(BASE_PATH, f'{new_id}-{resume["fullname"]}')
        setattr(value, 'path', path)
        os.mkdir(path)
        
    users = db.session.query(User).filter(User.role.in_(['superuser', 'user']), 
                                                        User.region_id == location_id).all()
    for user in users:
        db.session.add(Message(message=f'Поступила анкета {resume["resume"]["fullname"]}', 
                               user_id=user.id))
    db.session.commit()

    resume_data(new_id, resume['document'], resume['addresses'], 
                resume['contacts'], resume['workplaces'], resume['staff'])
    return '', 200


@bp.post('/api/v1/check')
@bp.input(CheckSchema)
@bp.auth_required(auth)
def check_in(response):
    
    candidate = db.session.query(Person).get(response['id'])
    del response['id']
    latest_check = db.session.query(Check).filter_by(person_id=candidate.id).order_by(Check.id.desc()).first()
    officer_id = db.session.query(User.id).filter_by(username=latest_check.officer).one_or_none().scalar()
    
    for k, v in response.items():
        setattr(latest_check, k, v)
    
    db.session.add(Message(message=f'Проверка кандидата {candidate.fullname} окончена', user_id=officer_id))
    
    if os.path.isdir(response['path']):
        if not os.path.isdir(latest_check.path):
            path = os.path.join(BASE_PATH, f'{candidate.id}-{candidate["fullname"]}')
            os.mkdir(path)
            check_path = os.path.join(path, {datetime.now().strftime("%Y-%m-%d")})
            os.mkdir(check_path)
        try:
            for file in os.listdir(response['path']):
                shutil.copyfile(file, latest_check.path)
        except FileNotFoundError as error:
            db.session.add(Message(message=error, user_id=officer_id))

    candidate.status = Status.reply.value
    db.session.commit()
    
    return '', 200

