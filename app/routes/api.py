import os
import shutil

import requests

from datetime import date, datetime
import requests

from apiflask import HTTPBasicAuth
from ..routes import bp
from ..extensions.extension import BASE_PATH, URL_CHECK, resume_data
from ..models.model import db, User, Candidate, Check, CheckSchema, DeserialResume, \
    serial_resume
from ..forms.form import Status

auth = HTTPBasicAuth()  # create the auth object


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
    if db.session.query(User).filter_by(username=username, password=password).first():
        # Return the user's username if successful
        return username
    # Return None if authentication fails
    return None


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
    resume['resume']['status'] = Status.NEWFAG.value
    resume['resume']['deadline'] = date.today()

    # Check if the same resume already exists in the database
    candidate = db.session.query(Candidate).filter(
        Candidate.fullname.ilike(f"{resume['resume']['fullname']}"),
        Candidate.birthday == resume['resume']['birthday']
    ).first()

    if candidate:  # If the resume already exists, update it
        for k, v in resume['resume'].items():
            setattr(candidate, k, v)
        new_id = candidate.id
    else:  # If the resume does not exist, create a new record
        value = Candidate(**resume['resume'])
        db.session.add(value)
        db.session.flush()
        new_id = int(value.id)

    # Store the rest of the resume data in the database
    resume_data(new_id, resume['document'], resume['addresses'], resume['contacts'], resume['workplaces'],
                resume['staff'])

    # Serialize the resume and send it for checking
    serialize = serial_resume.decer_res(new_id, officer='API')
    response = requests.post(url=URL_CHECK, json=serialize, timeout=5)
    response.raise_for_status()

    # Update the resume status based on the response from the checking service
    # Commit changes to the database and return the stored resume
    result = db.session.query(Candidate).filter_by(id=new_id).first()
    if response.status_code == 200:
        result.status = Status.AUTO.value
        db.session.commit()
        return {'status': 201}
    else:
        result.status = Status.NEWFAG.value
        db.session.commit()
        return {'status': 202}


@bp.post('/api/v1/check')
@bp.input(CheckSchema)
@bp.auth_required(auth)
def checkin(response):
    """
    Receives a JSON payload containing information about a candidate check,
    including the candidate ID and status. If the status is REPLY, it copies
    files from a source directory to a destination directory, sets the
    candidate's status to REPLY, and creates a new check record. If the status
    is not REPLY, it sets the candidate's status to ERROR.

    :param response: A dictionary containing the following keys: id (int),
        autostatus (str), path (str), and any other keys required by the
        CheckSchema.
    :return: A dictionary containing a message string.
    """
    result = db.session.get(Candidate, response['id'])
    if response['autostatus'] == Status.REPLY.value:
        # Set the candidate's status to REPLY.
        result.status = Status.REPLY.value
        # Create a path for the candidate's files.
        path = os.path.join(
            BASE_PATH, result.fullname[0], f"{str(result.id)}-{result.fullname}",
            datetime.now().strftime("%Y-%m-%d"))
        # Copy files from the source directory to the destination directory.
        try:
            for file in os.listdir(response['path']):
                print(file)
                shutil.copyfile(file, path)
        except FileNotFoundError as e:
            response['autostatus'] = f'{e}'
        # Update the response dictionary with the candidate ID and path.
        response["cand_id"] = response.pop('id')
        response["path"] = path
        # Create a new check record.
        check_dict = response | {"deadline": datetime.now()}
        db.session.add(Check(**check_dict))
    else:
        # Set the candidate's status to ERROR.
        result.status = Status.ERROR.value
    db.session.commit()
    # Return a message confirming the response was received.
    return {'status': 201}
