from datetime import datetime
import shutil
import os

import bcrypt
from apiflask import HTTPBasicAuth

from ..routes import bp
from ..utils.excel import resume_data, BASE_PATH
from ..models.model import db, User, Candidate, Check, Message, Status
from ..models.schema import CheckSchema, ResumeSchema

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str):
    user = db.session.query(User).filter_by(username=username).one_or_none()
    if user and not user.blocked:
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return username


@bp.post('/api/v1/anketa')
@bp.input(ResumeSchema)
@bp.auth_required(auth)
def anketa(resume: dict):
    resume['resume']["request_id"] = resume['resume'].pop('id')
    candidate = db.session.query(Candidate).filter(
        Candidate.fullname.ilike(f"{resume['resume']['fullname']}"),
        Candidate.birthday == datetime.strptime(resume['resume']['birthday'], "%Y-%m-%d")
    ).one_or_none()

    if candidate:
        resume['resume']['status'] = Status.update.value
        resume['resume']['update'] = datetime.now()
        for k, v in resume['resume'].items():
            setattr(candidate, k, v)
        new_id = candidate.id
    else:
        value = Candidate(**resume['resume'])
        db.session.add(value)
        db.session.flush()
        new_id = value.id
    db.session.commit()

    resume_data(new_id, resume['document'], resume['addresses'], 
                resume['contacts'], resume['workplaces'], resume['staff'])
    return '', 201


@bp.post('/api/v1/check')
@bp.input(CheckSchema)
@bp.auth_required(auth)
def check_in(response):
    candidate = db.session.query(Candidate).get(response['id'])
    del response['id']
    candidate.status = Status.reply.value
    path = os.path.join(
        BASE_PATH, candidate.fullname[0], f"{str(candidate.id)}-{candidate.fullname}",
        datetime.now().strftime("%Y-%m-%d"))
    latest_check = db.session.query(Check).filter_by(cand_id=candidate.id).order_by(Check.id.desc()).first()
    officer_id = db.session.query(User.id).filter_by(username=latest_check.officer).one_or_none()
    for k, v in response.items():
        setattr(latest_check, k, v)
    db.session.add(Message(message=f'Проверка кандидата {candidate.fullname} окончена', user_id=officer_id))
    if response['path']:
        try:
            for file in os.listdir(response['path']):
                shutil.copyfile(file, path)
        except FileNotFoundError as error:
            db.session.add(Message(message=error, user_id=officer_id))
    db.session.commit()
    return '', 201

