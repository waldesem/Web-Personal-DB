from .. import scheduler

from models.model import db, Person, OneS

# @scheduler.task('cron', id='get_id')
def match_id():
    staffs = db.session.query(OneS).all()
    if len(staffs):
        for staff in staffs:
            person_id =  db.session.query(Person.id).\
                filter_by(fullname=staff.full_name, 
                        birthday=staff.birth_date).one_or_none()
            if person_id:
                staff.person_id = person_id
        db.session.commit()