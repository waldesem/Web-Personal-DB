import os
from datetime import datetime

from flask import current_app
from ..models.model import db, Staff, Document, Address, Contact, Workplace, Person
from ..models.classes import Status


def resume_data(person_id, document, addresses, contacts, workplaces, staff):
    """
    Adds resume data to the database for a person.
    """
    db.session.add(Staff(**staff | {'person_id': person_id}))
    db.session.add(Document(**document | {'person_id': person_id}))
    for address in addresses:
        db.session.add(Address(**address | {'person_id': person_id}))
    for contact in contacts:
        db.session.add(Contact(**contact | {'person_id': person_id}))
    for workplace in workplaces:
        db.session.add(Workplace(**workplace | {'person_id': person_id}))
    db.session.commit()


def add_resume(resume: dict, location_id, action):
    """
    Adds a resume to the database.
    """
    result = db.session.query(Person).\
        filter(Person.fullname.ilike(resume['fullname']),
               Person.birthday==resume['birthday']).one_or_none()
    if result:
        if action == "create" or action == 'api':
            resume.update({'status': Status.repeat.value, 'region_id': location_id})
        else:
            resume.update({'status': Status.update.value, 'region_id': location_id})
        for k, v in resume.items():
            setattr(result, k, v)
        person_id = result.id
        
        if result.path and not os.path.isdir(result.path):
            os.mkdir(result.path)
        elif not result.path:
            new_path = os.path.join(current_app.config["BASE_PATH"], 
                                    f'{person_id}-{resume["fullname"]}')
            if not os.path.isdir(new_path):
                os.mkdir(new_path)
            result.path = new_path
    else:
        person = Person(**resume | {'region_id': location_id})
        db.session.add(person)
        db.session.flush()
        person_id = person.id
        
        path = os.path.join(current_app.config["BASE_PATH"], 
                            f'{person_id}-{resume["fullname"]}')
        person.path = path
        if not os.path.isdir(path):
            os.mkdir(path)
        
    db.session.commit()
    return person_id


def create_folders(person_id, fullname, folder_name):
    """
    Check if a folder exists for a given person and create it if it does not exist.
    """
    url = os.path.join(current_app.config["BASE_PATH"], f'{person_id}-{fullname}')
    if not os.path.isdir(url):
        os.mkdir(url)
    folder = os.path.join(url, folder_name)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    subfolder = os.path.join(folder, datetime.now().strftime("%Y-%m-%d"))
    if not os.path.isdir(subfolder):
        os.mkdir(subfolder)
    return subfolder
