from models.model import db, Person

def get_id(fullname, birth_date):
    return db.session.query(Person.id).filter_by(fullname=fullname, 
                                            birth_date=birth_date).first()