import shutil
import os
import re

import bcrypt
from apiflask import HTTPBasicAuth
# from flask_mailing import Message 

from ..routes import bp
# from ..mail.mail import mail
from ..routes.route import add_resume, folder_check
from ..utils.excel import resume_data
from ..models.model import db, User, Person, Region, Check, Report, Status
from ..models.schema import CheckSchema, ResumeSchema
from ..models.classify import Role

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str):
    user = db.session.query(User).filter_by(username=username).one_or_none()
    if user and not user.blocked and user.has_role(Role.api.value):
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return ''


@bp.post('/api/v1/anketa')
@bp.input(ResumeSchema)
@bp.auth_required(auth)
def anketa(anketa: dict):
    resume = anketa['resume']
    resume["request_id"] = resume.pop('id')
    
    regions = {rgn[1][1]: rgn[0][1] for rgn in db.session.guery(Region.id, Region.region).all()}
    division = re.split(r'/', resume['staff']['department'])
    location_id = 1
    for div in division:
        if div.strip() in regions:
            location_id = regions.values[div]
            
    person_id, result = add_resume(resume, location_id)
        
    users = db.session.query(User).filter(User.role.in_(['superuser', 'user']), 
                                                        User.region_id == location_id).all()
    for user in users:
        # message = Message(subject="Новая анкета",
        #                   recipients=[user.email],
        #                   body=f'<p>Поступила анкета {resume["fullname"]}</p>',
        #                   subtype="html")
        # await mail.send_message(message)

        db.session.add(Report(message=f'Поступила анкета {resume["fullname"]}', 
                               user_id=user.id))
    db.session.commit()

    resume_data(person_id, resume['document'], resume['addresses'], 
                resume['contacts'], resume['workplaces'], resume['staff'])
    return bool(result), 200


@bp.post('/api/v1/check')
@bp.input(CheckSchema)
@bp.auth_required(auth)
def check_in(response):
    candidate = db.session.query(Person).get(response['id'])
    del response['id']
    latest_check = db.session.query(Check).filter_by(person_id=candidate.id).order_by(Check.id.desc()).first()
    user = db.session.query(User).filter_by(username=latest_check.officer).one_or_none().scalar()
    
    db.session.add(Report(message=f'Проверка кандидата {candidate.fullname} окончена', user_id=user.id))
    # message = Message(subject="Результаты проверки",
    #                   recipients=[user.email],
    #                   body=f'<p>Проверка кандидата {candidate.fullname} окончена</p>',
    #                   subtype="html")
    # await mail.send_message(message)

    if os.path.isdir(response['path']):
        check_path = latest_check.path if os.path.isdir(latest_check.path) else folder_check(candidate.id, candidate["fullname"])
        response.update({'path': check_path})
        try:
            for file in os.listdir(response['path']):
                shutil.copyfile(file, check_path)
        except FileNotFoundError as error:
            db.session.add(Report(message=error, user_id=user.id))
    
    for k, v in response.items():
        setattr(latest_check, k, v)
    
    candidate.status = Status.reply.value
    db.session.commit()
    
    return '', 200

