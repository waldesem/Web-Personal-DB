from .. import scheduler

from models.model import db, Report, Person, OneS, User
from models.classes import Reports

# @scheduler.task('cron', id='get_id')
def match_id():
    ones = db.session.query(OneS).all()
    if len(ones):
        for one in ones:
            person_id =  db.session.query(Person.id).\
                filter_by(fullname=one.full_name, 
                        birthday=one.birth_date).one_or_none()
            if person_id:
                one.person_id = person_id
        admins = db.session.query(User).all()
        for admin in admins:
            if admin.has_role('admin'):
                db.session.add(Report(category=Reports.middle.value,
                                    report='Успешно импортированы данные из 1С', 
                                    user_id=admin.id))
        db.session.commit()
