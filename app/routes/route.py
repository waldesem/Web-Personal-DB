import json
import os
from datetime import datetime
import requests

from sqlalchemy import func
from flask import render_template, request
from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest

from . import bp
from ..extensions.extension import ExcelFile, resume_data, URL_CHECK, BASE_PATH
from ..models.model import Candidate, Staff, Document, Address, Contact, Workplace, RelationShip, \
    Check, Registry, Poligraf, Investigation, Inquiry, TODAY, Status, db, resume_schema, \
    staff_schema, document_schema, address_schema, contact_schema, work_schema, relation_schema, \
    check_schema, poligraf_schema, registry_schema, investigation_schema, inquiry_schema


@bp.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400


@bp.get('/')
def main():
    """
    A function that serves the main page of the web application.
    Returns:
        The HTML page for the index.
    """
    return render_template("index.html")


@bp.route('/index/<flag>/<int:page>', methods=['GET', 'POST'])  # Flask route decorator
@bp.doc(hide=True)  # Flask API documentation decorator
@login_required  # Flask-Login authentication decorator
def index(flag, page):
    """
    Renders the index page with a list of candidates based on the selected flag and page number.
    :param flag: A string representing the selected flag ('main', 'new', 'officer', or anything else).
    :param page: An integer representing the selected page number.
    :return: A list of candidate data and pagination information wrapped in a dictionary.
    """
    pagination = 12  # Number of candidates per page
    if flag == 'main':  # Show all candidates, ordered by ID in descending order
        title = "Главная страница"
        query = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                                 Candidate.status, Candidate.deadline).order_by(Candidate.id.desc()). \
            paginate(page=page, per_page=pagination, error_out=False)
    elif flag == 'new':  # Show only candidates with status NEWFAG, ordered by ID in descending order
        title = "Новые анкеты"
        query = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                                 Candidate.status, Candidate.deadline).filter_by(status=Status.NEWFAG.value). \
            order_by(Candidate.id.desc()).paginate(page=page, per_page=pagination, error_out=False)
    elif flag == 'officer':  # Show candidates where the current user is the assigned officer, ordered by ID
        title = "Страница пользователя"
        query = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                                 Candidate.status, Candidate.deadline).filter(Candidate.status.notin_(
            [Status.FINISH.value, Status.RESULT.value, Status.CANCEL.value])). \
            join(Check, isouter=True).filter_by(officer=current_user.username).order_by(Candidate.id.asc()). \
            paginate(page=page, per_page=pagination, error_out=False)
    else:  # Search for candidates based on submitted form data, ordered by ID in ascending order
        title = "Страница поиска"
        query = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                                 Candidate.status, Candidate.deadline).filter(
            Candidate.region.ilike('%{}%'.format(request.form.get('region', ''))),
            Candidate.fullname.ilike('%{}%'.format(request.form.get('fullname', ''))),
            Candidate.birthday.ilike('%{}%'.format(request.form.get('birthday', ''))),
            Candidate.status.ilike('%{}%'.format(request.form.get('status', ''))),
        ).order_by(Candidate.id.asc()).paginate(page=page, per_page=pagination, error_out=False)

    # Serialize candidate data using the ResumeSchema schema
    datas = resume_schema.dump(query, many=True)

    # Determine if there is a next and/or previous page
    has_next, has_prev = int(query.has_next), int(query.has_prev)

    # Return serialized candidate data and pagination information wrapped in a dictionary
    return [datas, {'has_next': has_next, "has_prev": has_prev, 'title': title}]


@bp.get('/count')
@bp.doc(hide=True)  # Flask API documentation decorator
@login_required  # Flask-Login authentication decorator
def get_count():
    """
    Returns a JSON object containing the total number of candidates in the database with status NEWFAG and the number of 
    candidates that have not been FINISHed, RESULTed, or CANCELled and have a Check officer that is the current user.
    :return: A JSON object containing 'news' and 'checks' keys.
    :rtype: dict
    """
    news = db.session.query(func.count(Candidate.status)).filter_by(
        status=Status.NEWFAG.value).scalar()  # Total number of candidates in the database with status NEWFAG
    checks = db.session.query(Candidate.id).filter(Candidate.status.notin_([
        Status.FINISH.value, Status.RESULT.value, Status.CANCEL.value
        ])).join(Check, isouter=True).filter_by(officer=current_user.username).scalar()
    return {'news': news, 'checks': checks}


@bp.post('/resume/create')
@bp.doc(hide=True)
@login_required
def post_resume():
    """
    Create or update a candidate's resume based on the form data in the request.
    Returns:
        A dictionary with the candidate's ID and a message indicating if a new record was created or an existing one was updated
    """
    # Get the form data as a dictionary
    resume_dict: dict = request.form.to_dict()

    # Query the database for a candidate with the same name and birthday
    result = db.session.query(Candidate).filter_by(fullname=resume_dict['fullname'],
                                                   birthday=resume_dict['birthday']).first()

    # Convert the birthday string to a datetime object
    resume_dict['birthday'] = datetime.strptime(resume_dict.pop('birthday'), "%Y-%m-%d")

    if result:
        # If a candidate with the same name and birthday already exists, update their record
        resume_dict.update({'status': Status.UPDATE.value})
        for k, v in resume_dict.items():
            setattr(result, k, v)
            db.session.commit()
        cand_id = result.id
        message = 'Запись уже существует. Данные обновлены'
    else:
        # If no candidate with the same name and birthday exists, create a new record
        resume_dict.update({'status': Status.NEWFAG.value, 'deadline': TODAY})
        value = Candidate(**resume_dict)
        db.session.add(value)
        db.session.flush()
        cand_id = value.id
        db.session.commit()
        message = 'Создана новая запись'

    # Return a dictionary with the candidate's ID and a message indicating if a new record was created or an existing
    # one was updated
    return {'cand_id': cand_id, 'message': message}


@bp.get('/profile/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def get_profile(cand_id):
    """
    Returns the full profile of a candidate/employee based on the candidate ID
    """
    # Querying the Candidate table for candidate with the provided ID
    cand = db.session.query(Candidate).filter_by(id=cand_id).all()
    # Serializing the candidate object(s) to a dictionary
    candidate = resume_schema.dump(cand, many=True)

    # Querying the Document table for all documents belonging to the candidate with the provided ID
    doc = db.session.query(Document).filter_by(cand_id=cand_id).order_by(Document.cand_id.asc()).all()
    # Serializing the document object(s) to a dictionary
    documents = document_schema.dump(doc, many=True)

    # Querying the Address table for all addresses belonging to the candidate with the provided ID
    addr = db.session.query(Address).filter_by(cand_id=cand_id).order_by(Address.id.asc()).all()
    # Serializing the address object(s) to a dictionary
    address = address_schema.dump(addr, many=True)

    # Querying the Contact table for all contacts belonging to the candidate with the provided ID
    cont = db.session.query(Contact).filter_by(cand_id=cand_id).order_by(Contact.id.asc()).all()
    # Serializing the contact object(s) to a dictionary
    contacts = contact_schema.dump(cont, many=True)

    # Querying the Workplace table for all workplaces belonging to the candidate with the provided ID
    work = db.session.query(Workplace).filter_by(cand_id=cand_id).order_by(Workplace.id.asc()).all()
    # Serializing the workplace object(s) to a dictionary
    workplaces = work_schema.dump(work, many=True)

    # Querying the RelationShip table for all relationships belonging to the candidate with the provided ID
    rel = db.session.query(RelationShip).filter_by(cand_id=cand_id).order_by(RelationShip.id.asc()).all()
    # Serializing the relationship object(s) to a dictionary
    relations = relation_schema.dump(rel, many=True)

    # Querying the Staff table for all staff belonging to the candidate with the provided ID
    staff = db.session.query(Staff).filter_by(cand_id=cand_id).order_by(Staff.id.asc()).all()
    # Serializing the staff object(s) to a dictionary
    staffs = staff_schema.dump(staff, many=True)

    # Querying the Check table for all checks belonging to the candidate with the provided ID
    check = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.asc()).all()
    # Serializing the check object(s) to a dictionary
    checks = check_schema.dump(check, many=True)

    # Querying the Registry table for all registries belonging to the checks of the candidate with the provided ID
    reg = [db.session.query(Registry).filter(Registry.check_id == i.id).first() for i in check]
    # Serializing the registry object(s) to a dictionary
    registries = registry_schema.dump(reg, many=True)

    # Querying the Poligraf table for all poligrafs belonging to the candidate with the provided ID
    pfo = db.session.query(Poligraf).filter_by(cand_id=cand_id).order_by(Poligraf.id.asc()).all()
    # Serializing the poligraf object(s) to a dictionary
    pfos = poligraf_schema.dump(pfo, many=True)

    # Querying the Investigation table for all investigations belonging to
    inv = db.session.query(Investigation).filter_by(cand_id=cand_id).order_by(Investigation.id.asc()).all()
    # Serializing the investigation object(s) to a dictionary
    invs = investigation_schema.dump(inv, many=True)

    # Querying the Inquiry table for all inquiries belonging to the candidate with the provided ID
    inq = db.session.query(Inquiry).filter_by(cand_id=cand_id).order_by(Inquiry.id.asc()).all()
    # Serializing the inquiry object(s) to a dictionary
    inquiries = inquiry_schema.dump(inq, many=True)

    # Return a list of dictionaries containing the candidate's information
    return [[candidate, staffs, documents, address, contacts, workplaces, relations],
            checks, registries, pfos, invs, inquiries, {i.name: i.value for i in Status}]


@bp.post('/resume/upload')
@bp.doc(hide=True)
@login_required
def upload_file():
    """
    Uploads a resume file and creates or updates a candidate record in the database

    Returns:
    A dictionary containing the candidate ID and a message indicating whether a new record was created or an existing
    record was updated
    """
    # Step 1: Retrieve the uploaded file
    file = request.files['file']

    # Step 2: Parse the Excel file
    excel = ExcelFile(file)

    # Step 3: Check if a candidate record already exists for the given name and birthday
    result = db.session.query(Candidate).filter(Candidate.fullname.ilike(excel.resume['fullname']),
                                                Candidate.birthday == (excel.resume['birthday'])).first()

    if result:  # If a record already exists, update it with the new data
        # Step 4: Update the candidate's basic information
        resum = excel.resume | {'status': Status.NEWFAG.value, 'deadline': TODAY}
        for k, v in resum.items():
            setattr(result, k, v)
            db.session.commit()

        # Step 5: Add new data to the candidate's record
        resume_data(result.id, excel.passport, excel.addresses, excel.contacts,
                    excel.workplaces, excel.staff)

        message = 'Запись уже существует. Данные обновлены'
    else:  # If no record exists, create a new one
        # Step 4: Create a new candidate record
        result = Candidate(**excel.resume | {'status': Status.NEWFAG.value, 'deadline': TODAY})
        db.session.add(result)
        db.session.flush()

        # Step 5: Add new data to the candidate's record
        resume_data(result.id, excel.passport, excel.addresses, excel.contacts,
                    excel.workplaces, excel.staff)

        db.session.commit()
        message = 'Создана новая запись'

    # Step 6: Return the candidate ID and message
    return {'cand_id': result.id, 'message': message}


@bp.post('/update/<flag>/<cand_id>')
@bp.doc(hide=True)
@login_required
def update_profile(flag, cand_id):
    """
    Updates the profile of the candidate with the given ID by adding a new record to the specified table.

    Args:
        flag: A string indicating the table to update.
        cand_id: A string representing the ID of the candidate to update.

    Returns:
        A dictionary containing a success or error message.
    """
    model_map = {
        'staff': Staff,
        'document': Document,
        'address': Address,
        'contact': Contact,
        'workplace': Workplace,
        'relation': RelationShip,
    }
    model = model_map.get(flag)
    if not model:
        return {"message": "Возникла ошибка. Значение {}".format(flag.upper())}

    form_data: dict = request.form.to_dict()

    # If updating documents or relationships, convert the date string to a datetime object
    if flag == 'document' or flag == 'relation':
        form_data['issue' if flag == 'document' else 'birthday'] = \
            datetime.strptime(form_data.pop('issue' if flag == 'document' else 'birthday'), "%Y-%m-%d")

    # Add the new record to the specified table using the SQLAlchemy model
    db_add_record(model, form_data, cand_id)

    return {"message": " Запись {} успешно добавлена".format(flag.upper())}


def db_add_record(Model, form_data, cand_id):
    """
    Add a new record to the database.
    :param Model: SQLAlchemy model of the table to insert into.
    :type Model: SQLAlchemy model
    :param form_data: Data to insert into the new record.
    :type form_data: dict
    :param cand_id: ID of the candidate associated with the new record.
    :type cand_id: int
    """
    db.session.add(Model(**form_data | {'cand_id': cand_id}))
    db.session.commit()


@bp.get('/resume/send/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def send_resume(cand_id):
    """
    Sends a resume for a candidate with the given ID.
    Args:
        cand_id: The ID of the candidate to send the resume for.
    Returns:
        A dictionary containing a message indicating the status of the resume send attempt.
    """
    # Get the candidate's resume
    resume = db.session.query(Candidate).get(cand_id)

    # Check the candidate's resume status to make sure it can be sent
    if resume.status in [Status.NEWFAG.value, Status.UPDATE.value]:
        decer = {'cand_id': cand_id, 'officer': current_user.username}

        try:
            # Send a request to check if the resume can be sent
            response = requests.post(url=URL_CHECK, json=decer, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            return {'message': f"Отправка не удалась. Попробуйте позднее ({e})"}
        else:
            if response.status_code == 200:
                # If the resume can be sent, update its status and commit the changes to the database
                resume.status = Status.ROBOT.value
                db.session.commit()
                return {'message': "Анкета успешно отправлена"}
            else:
                # If the resume cannot be sent, return an error message
                return {'message': "Отправка не удалась. Попробуйте позднее"}
    else:
        # If the resume cannot be sent, return an error message
        return {'message': "Анкета не может быть отправлена. Проверка уже начата"}


@bp.get('/resume/status/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def patch_status(cand_id: int) -> dict:
    """Updates a Candidate's status to 'UPDATE' and sets the 'deadline' to today's date.
    Args:
        cand_id (int): The ID of the Candidate to update.
    Returns:
        dict: A dictionary containing a message indicating whether the update was successful.
    """
    # Query the database for the Candidate with the given ID
    result = db.session.query(Candidate).filter_by(id=cand_id).one_or_none()

    # If the Candidate exists and its status is not a final status (e.g. 'RESULT' or 'POLIGRAF')
    if result and result.status not in (Status.RESULT.value, Status.POLIGRAF.value):
        # Update the Candidate's status to 'UPDATE' and set the 'deadline' to today's date
        result.status = Status.UPDATE.value
        result.deadline = TODAY
        db.session.commit()
        return {"message": "Статус обновлен"}  # Return a success message
    else:
        return {"message": "Текущий статус обновить нельзя"}  # Return an error message


@bp.post('/check/<flag>/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def post_check(flag: str, cand_id: int) -> dict:
    """
    Perform a post request to check a candidate.
    Args:
        cand_id (int): The id of the candidate to check.
    Returns:
        dict: A dictionary containing a message indicating the success of the check.
        :param cand_id:
        :param flag:
    """
    # Get the candidate from the database
    candidate = db.session.query(Candidate).get(cand_id)
    # Get the data from the html form
    check_form: dict = request.form.to_dict()
    check_form['deadline'] = datetime.strptime(check_form.pop('deadline'), "%Y-%m-%d")
    check_form['pfo'] = bool(check_form.pop('pfo')) if 'pfo' in check_form else False

    if flag == 'new':
        # Create a path for the check materials
        path = os.path.join(BASE_PATH, candidate.fullname[0], f"{str(candidate.id)}-{candidate.fullname}",
                            TODAY.strftime("%Y-%m-%d"))
        # Convert the form data to a dictionary and update the path and candidate id
        check_form.update({'path': path, "cand_id": cand_id, 'officer': current_user.username})
        
        # Add the check to the database
        db.session.add(Check(**check_form))
        db.session.commit()
    else:
        check_form.update({"cand_id": cand_id, 'officer': current_user.username})

        latest_check = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.desc()).first()
        # Add the check to the database
        for k, v in check_form.items():
            setattr(latest_check, k, v)
            db.session.commit()
    
    # Determine the conclusion of the check and update the candidate's status
    conclusion = check_form['conclusion']
    if conclusion == Status.SAVE.value:
        candidate.status = Status.SAVE.value
        message = "Проверка успешно сохранена"
    elif conclusion == Status.CANCEL.value:
        candidate.status = Status.CANCEL.value
        message = "Проверка отменена"
    else:
        candidate.status = Status.POLIGRAF.value if check_form['pfo'] else Status.RESULT.value
        message = "Проверка завершена. Назначено проведение ПФО" if check_form['pfo'] else "Проверка завершена"
    db.session.commit()
    
    # Return a message indicating the success of the check
    return {'message': message}


@bp.get('/check/delete/<int:cand_id>')
@login_required
def delete_check(cand_id):
    """
    Deletes the latest check for a candidate, given their ID.
    Args:
        cand_id (int): The ID of the candidate whose check should be deleted.
    Returns:
        A dictionary with the key 'message' and a message indicating whether the deletion was successful.
    """
    # Retrieve the candidate and the latest check for this candidate
    candidate = db.session.query(Candidate).get(cand_id)
    latest_check = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.desc()).first()

    # Check if the candidate has a completed status
    if candidate.status is not None and candidate.status == Status.FINISH.value:
        # If the candidate has a completed status, return an error message indicating that the check cannot be deleted.
        return {'message': "Проверка с текущим статусом не может быть удалена"}

    # Delete the latest check for this candidate
    if latest_check is not None:
        db.session.delete(latest_check)
        db.session.commit()
        # If the deletion was successful, return a success message.
        return {'message': "Проверка успешно удалена"}
    else:
        # If the candidate has no checks, return a message indicating this.
        return {'message': "Кандидат ранее не проверялся"}


@bp.get('/check/status/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def status_check(cand_id):  # запрашиваем данные проверки
    """
    This function retrieves the status of a candidate's application.
    Args:
        cand_id (int): The ID of the candidate to retrieve the status for.
    Returns:
        A JSON object containing the status of the candidate's application.
    """
    # Retrieve candidate from the database
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()

    # Check if the candidate's status is currently being processed
    if candidate.status != Status.NEWFAG.value and candidate.status != Status.UPDATE.value:
        message = "Анкета взята в работу и еще не закончена"
    else:
        # If the candidate's status is not being processed, set it to manual and commit changes to the database
        candidate.status = Status.MANUAL.value
        db.session.commit()
        message = "Начата ручная проверка"

    # Return a JSON object containing the message to be displayed to the user
    return {'message': message}


@bp.post('/registry/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def post_registry(cand_id):
    """Endpoint for posting a candidate's registry information"""
    form_registry = request.form.to_dict()  # Load approval form
    result = db.session.query(Check).filter_by(cand_id=cand_id).order_by(
        Check.id.desc()).first()  # Get the latest check for the candidate
    reg = {
        'check_id': result.id,
        'supervisor': current_user.username,
        'deadline': TODAY,
        **form_registry
    }
    db.session.add(Registry(**reg))  # Add registry information to the database
    db.session.commit()
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()  # Get candidate information
    # response = requests.post(url=URL_CHECK, json=json.dumps(
    #     {
    #         "id": candidate.request_id,
    #         "comments": reg['comments'],
    #         "decision": reg['decision'],
    #         "deadline": TODAY.strftime("%Y-%m-d%"),
    #         "supervisor": reg['supervisor']
    #     }
    # ), timeout=5)
    # response.raise_for_status()
    # if response.status_code == 200:  # Check if the response was successfully sent
    candidate.status = Status.CANCEL.value if reg['decision'] == Status.CANCEL.value else Status.FINISH.value
    # Update candidate status based on decision
    db.session.commit()
    return {'message': "Решение успешно отправлено"}  # Return success message
    # else:
    #     return {'message': 'Отправка не удалась попробуйте еще раз позднее'}  # Return failure message


@bp.post('/poligraf/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def post_poligraf(cand_id):
    """
    View function that handles the Poligraf POST request for a candidate.
    Args:
        cand_id (int): The candidate ID.
    Returns:
        dict: A dictionary containing the message "Запись успешно добавлена".
    """
    # Retrieve the form data and convert the deadline string to a datetime object.
    form_poligraf: dict = request.form.to_dict()
    form_poligraf['deadline'] = datetime.strptime(form_poligraf.pop('deadline'), "%Y-%m-%d")

    # Create a new Poligraf object and add it to the database.
    poligraf = Poligraf(**form_poligraf, cand_id=cand_id, officer=current_user.username)
    db.session.add(poligraf)
    db.session.commit()

    # Update the status of the candidate if necessary.
    candidate = Candidate.query.get(cand_id)
    if candidate.status == Status.POLIGRAF.value:
        candidate.status = Status.RESULT.value
        db.session.commit()

    # Return a success message.
    return {"message": "Запись успешно добавлена"}


@bp.post('/investigation/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def post_investigation(cand_id):
    """
    Adds a new investigation to the database for a given candidate.
    Args:
        cand_id (int): The ID of the candidate to add the investigation for.
    Returns:
        dict: A dictionary containing a success message.
    """
    # Get data from the form
    form_investigation: dict = request.form.to_dict()

    # Convert the deadline string to a datetime object
    form_investigation['deadline'] = datetime.strptime(form_investigation.pop('deadline'), "%Y-%m-%d")

    # Add the investigation to the database
    db.session.add(Investigation(**form_investigation | {'cand_id': cand_id}))
    db.session.commit()

    # Return a success message
    return {"message": "Запись успешно добавлена"}


@bp.post('/inquiry/<int:cand_id>')
@bp.doc(hide=True)
@login_required
def post_inquiry(cand_id):
    """
    This function handles a POST request to add an inquiry for a candidate.
    Args:
        cand_id (int): The ID of the candidate to add the inquiry for.
    Returns:
        dict: A dictionary containing a success message.
    """
    # Get the form data as a dictionary
    form_inquiry: dict = request.form.to_dict()

    # Convert the 'deadline' string to a datetime object and update the form data
    form_inquiry['deadline'] = datetime.strptime(form_inquiry.pop('deadline'), "%Y-%m-%d")

    # Create a new Inquiry object with the form data and candidate ID, and add it to the database session
    db.session.add(Inquiry(**form_inquiry | {'cand_id': cand_id}))

    # Commit the changes to the database
    db.session.commit()

    # Return a success message
    return {"message": "Запись успешно добавлена"}


@bp.post('/information')
@bp.doc(hide=True)
def post_information():
    """
    Retrieve statistics for a given period of time.
    Returns:
        A dictionary containing candidate and poligraf statistics, as well as a title for the statistics.
    """
    # Retrieve data from the form submission
    statistic = request.form.to_dict()

    # Retrieve candidate statistics from the database
    candidates = db.session.query(
        Registry.decision,
        func.count(Registry.id)
    ).group_by(
        Registry.decision
    ).filter(
        Registry.deadline.between(statistic['start'], statistic['end'])
    ).all()

    # Retrieve poligraf statistics from the database
    pfo = db.session.query(
        Poligraf.theme,
        func.count(Poligraf.id)
    ).group_by(
        Poligraf.theme
    ).filter(
        Poligraf.deadline.between(statistic['start'], statistic['end'])
    ).all()

    # Return a dictionary containing the candidate and poligraf statistics as well as a title for the statistics
    return {
        "candidates": [dict([cand]) for cand in candidates],
        "poligraf": [dict([test]) for test in pfo],
        "title": f'Cтатистика за период c {statistic["start"]} по {statistic["end"]}'
    }
