from datetime import date, datetime

import requests
from apiflask import HTTPBasicAuth
from flask_jwt_extended import current_user

from ..routes import bp
from ..utils.check import check_result
from ..utils.excel import resume_data
from ..models.model import db, User, Candidate, Message, CheckSchema, DeserialResume, \
    Status, serial_resume

auth = HTTPBasicAuth()  # create the auth object
TODAY = datetime.now()


@auth.verify_password
def verify_password(username: str, password: str):
    """
    Verify the user's password.
    Args:
        username (str): The user's username.
        password (str): The user's password.
    Returns:
        str: The user's username if successful, otherwise None.
    """
    # Check if the user exists in the database
    return db.session.query(User.fullname).filter_by(username=username, password=password).one_or_none()


@bp.post('/api/v1/anketa')
@bp.input(DeserialResume)
@bp.auth_required(auth)
def anketa(resume):
    """
    Receives a resume in JSON format and stores it in the database. Returns the stored resume.
    Parameters:
        resume (Dict[str, Any]): The resume to be stored.
    Returns:
        Dict[str, Any]: The stored resume.
    """
    # Rename 'id' key to 'request_id' and update status and deadline
    resume['resume']["request_id"] = resume['resume'].pop('id')

    # Check if the same resume already exists in the database
    candidate = db.session.query(Candidate).filter(
        Candidate.fullname.ilike(f"{resume['resume']['fullname']}"),
        Candidate.birthday == resume['resume']['birthday']
    ).first()

    if candidate:  # If the resume already exists, update it
        resume['resume']['status'] = Status.UPDATE.value
        resume['resume']['update'] = date.today()
        for k, v in resume['resume'].items():
            setattr(candidate, k, v)
        new_id = candidate.id
    else:  # If the resume does not exist, create a new record
        resume['resume']['status'] = Status.NEWFAG.value
        resume['resume']['create'] = date.today()
        value = Candidate(**resume['resume'])
        db.session.add(value)
        db.session.flush()
        new_id = int(value.id)

    # Store the rest of the resume data in the database
    resume_data(new_id, resume['document'], resume['addresses'], resume['contacts'], resume['workplaces'],
                resume['staff'])

    # Serialize the resume and send it for checking
    serialize = serial_resume.decer_res(new_id, officer='API')
    response = requests.post(url='URL_CHECK', json=serialize, timeout=5)
    response.raise_for_status()

    # Update the resume status based on the response from the checking service
    # Commit changes to the database and return the stored resume
    result = db.session.query(Candidate).filter_by(id=new_id).first()
    if response.status_code == 200:
        result.status = Status.AUTO.value
        db.session.commit()
        return {'status': 201}
    else:
        result.status = Status.ERROR.value
        db.session.commit()
        return {'status': 202}


@bp.post('/api/v1/check')
@bp.input(CheckSchema)
@bp.auth_required(auth)
def checkin(response):
    """
    Receives a JSON payload containing information about a candidate check,
    including the candidate ID and status.
    :param response: A dictionary containing the following keys: id (int),
        autostatus (str), path (str), and any other keys required by the
        CheckSchema.
    :return: A dictionary containing a message string.
    """
    result = check_result(response)
    resume = db.session.get(Candidate, response['id'])
    if result == "OK":
        db.session.add(Message(message=f'Проверка кандидата {resume.fullname} окончена', 
                            create=TODAY, user_id=current_user.id))
        db.session.commit()
    else:
        db.session.add(Message(message=f'Проверка кандидата {resume.fullname} не выполнена', 
                            create=TODAY, user_id=current_user.id))
        db.session.commit()
    # Return a message confirming the response was received.
    return {'status': 201}
