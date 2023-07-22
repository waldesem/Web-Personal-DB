from datetime import datetime
import shutil
import os

import bcrypt
from apiflask import HTTPBasicAuth

from ..routes import bp
from ..utils.excel import resume_data
from ..models.model import db, User, Person, Check, Message, Status
from ..models.schema import CheckSchema, ResumeSchema

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
    if user and not user.blocked and user.has_role('api'):
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return username


@bp.post('/api/v1/anketa')
@bp.input(ResumeSchema)
@bp.auth_required(auth)
def anketa(resume: dict):
    """
    This function handles the '/api/v1/anketa' endpoint for POST requests.
    It takes in a `resume` parameter of type `dict` which contains the resume details.
    The function first checks if a candidate with the same fullname and birthday exists in the database.
    If a candidate is found, the resume details are updated in the database.
    If no candidate is found, a new candidate is created with the given resume details.
    The function then commits the changes to the database and calls the `resume_data` function to process additional resume data.
    Finally, an empty string is returned.

    Parameters:
        - resume: A dictionary containing the resume details.
    
    Returns:
        - An empty string.
    """
    resume['resume']["request_id"] = resume['resume'].pop('id')
    candidate = db.session.query(Person).filter(
        Person.fullname.ilike(f"{resume['resume']['fullname']}"),
        Person.birthday == resume['resume']['birthday']
    ).one_or_none()

    if candidate:
        resume['resume']['status'] = Status.update.value
        resume['resume']['update'] = datetime.now()
        for k, v in resume['resume'].items():
            setattr(candidate, k, v)
        new_id = candidate.id
    else:
        value = Person(**resume['resume'])
        db.session.add(value)
        db.session.flush()
        new_id = value.id
    users = db.session.query(User).filter(User.role.in_(
        ['superuser', 'user']
        )).all()
    for user in users:
        db.session.add(Message(message=f'Поступила анкета {resume["resume"]["fullname"]}', 
                               user_id=user.id))
    db.session.commit()

    resume_data(new_id, resume['document'], resume['addresses'], 
                resume['contacts'], resume['workplaces'], resume['staff'])
    return ''


@bp.post('/api/v1/check')
@bp.input(CheckSchema)
@bp.auth_required(auth)
def check_in(response):
    """
    Handles the API endpoint for checking in a response.
    
    Args:
        response (dict): The response data sent by the client.
        
    Returns:
        str: An empty string.
    """
    candidate = db.session.query(Person).get(response['id'])
    del response['id']
    latest_check = db.session.query(Check).filter_by(person_id=candidate.id).order_by(Check.id.desc()).first()
    officer_id = db.session.query(User.id).filter_by(username=latest_check.officer).one_or_none()[0]
    for k, v in response.items():
        setattr(latest_check, k, v)
    db.session.add(Message(message=f'Проверка кандидата {candidate.fullname} окончена', user_id=officer_id))
    if response['path']:
        try:
            for file in os.listdir(response['path']):
                shutil.copyfile(file, latest_check.path)
        except FileNotFoundError as error:
            db.session.add(Message(message=error, user_id=officer_id))
    candidate.status = Status.reply.value
    db.session.commit()
    return ''

