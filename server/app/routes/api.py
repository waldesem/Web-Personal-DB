from datetime import date, datetime
import shutil
import os


from apiflask import HTTPBasicAuth
from flask_jwt_extended import current_user

from ..routes import bp
from ..utils.excel import resume_data, BASE_PATH
from ..models.model import db, User, Candidate, Check, Message, CheckSchema, DeserialResume, Status

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


@bp.post('/api/v1/check')
@bp.input(CheckSchema)
@bp.auth_required(auth)
def check_in(response):
    result = db.session.get(Candidate, response['id'])
    if response['autostatus'] == Status.REPLY.value:
        # Set the candidate's status to REPLY.
        result.status = Status.REPLY.value
        # Create a path for the candidate's files.
        path = os.path.join(
            BASE_PATH, result.fullname[0], f"{str(result.id)}-{result.fullname}",
            datetime.now().strftime("%Y-%m-%d"))
        # Copy files from the source directory to the destination directory.
        if response['path']:
            try:
                for file in os.listdir(response['path']):
                    shutil.copyfile(file, path)
            except FileNotFoundError as e:
                result.status = Status.ERROR.value
                response['autostatus'] = f'{e}'
                db.session.add(Message(message=result,
                               create=TODAY, user_id=current_user.id))
        # Update the response dictionary with the candidate ID and path.
        response["cand_id"] = response.pop('id')
        response["path"] = path
        # Create a new check record.
        check_dict = response | {"deadline": datetime.now()}
        db.session.add(Check(**check_dict))
        db.session.add(Message(message=f'Проверка кандидата {result.fullname} окончена', create=TODAY, user_id=current_user.id))
    else:
        # Set the candidate's status to ERROR.
        result.status = Status.ERROR.value
        db.session.add(Message(message=f'Проверка кандидата {result.fullname} не выполнена',
                               create=TODAY, user_id=current_user.id))
    db.session.commit()
    # Return a message confirming the response was received.
    return '', 201
