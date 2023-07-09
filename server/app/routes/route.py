import json
import os
from datetime import datetime
import requests
from flask_jwt_extended import current_user, jwt_required

from sqlalchemy import func, or_
from flask import request, send_from_directory
from werkzeug.exceptions import BadRequest

from . import bp

from ..utils.check import task_queue
from ..utils.excel import ExcelFile, resume_data, BASE_PATH
from ..models.model import AddressSchema, CandidateSchema, CheckSchema, ContactSchema, DocumentSchema, InquirySchema, InvestigationSchema, MessageSchema, PoligrafSchema, RegistrySchema, StaffSchema, WorkplaceSchema, db, Candidate, Staff, Document, Address, Contact, Workplace, \
    Check, Registry, Poligraf, Investigation, Inquiry, Status, Message

TODAY = datetime.now()

bp.static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dist'))


@bp.route('/', defaults={'path': ''})
@bp.route('/<string:path>')
@bp.route('/<path:path>')
@bp.route('/information')
@bp.route('/profile/<string:cand_id>')
@bp.doc(hide=True)
def main(path=''):
    """
    This function handles the main route of the application.
    Args:
        path (str): The path of the requested file.
    Returns:
        If the path exists, it returns the requested file from the static folder.
        Otherwise, it returns the index.html file.
    """
    if path and os.path.exists(os.path.join(bp.static_folder, path)):
        return send_from_directory(bp.static_folder, path)
    else:
        return bp.send_static_file('index.html')


@bp.route('/index/<flag>/<int:page>', methods=['GET', 'POST'])  # Flask route decorator
@bp.doc(hide=True)  # Flask API documentation decorator
@jwt_required()
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
                                 Candidate.status, Candidate.create).order_by(Candidate.id.desc()). \
            paginate(page=page, per_page=pagination, error_out=False)

    elif flag == 'new':  # Show only candidates with status NEWFAG, ordered by ID in descending order
        title = "Новые анкеты"
        query = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                                 Candidate.status, Candidate.create).filter(Candidate.status.in_([Status.NEWFAG.value,
                                                                                                  Status.UPDATE.value]))\
            .order_by(Candidate.id.desc()).paginate(page=page, per_page=pagination, error_out=False)

    elif flag == 'officer':  # Show candidates where the current user is the assigned officer, ordered by ID
        title = "Страница пользователя"
        query = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                                 Candidate.status, Candidate.create).filter(Candidate.status.notin_(
            [Status.FINISH.value, Status.RESULT.value, Status.CANCEL.value])). \
            join(Check, isouter=True).filter_by(officer=current_user.username).order_by(Candidate.id.asc()). \
            paginate(page=page, per_page=pagination, error_out=False)

    else:  # Search for candidates based on submitted form data, ordered by ID in ascending order
        title = "Страница поиска"
        search = request.get_json()
        print(search)
        query = db.session.query(Candidate.id, Candidate.region, Candidate.fullname, Candidate.birthday,
                                 Candidate.status, Candidate.create).filter(
            or_(Candidate.region.ilike('%{}%'.format(search['region'])), search['region'] == ''),
            or_(Candidate.fullname.ilike('%{}%'.format(search['fullname'])), search['fullname'] == ''),
            or_(Candidate.birthday.ilike('%{}%'.format(search['birthday'])), search['birthday'] == '')
        ).order_by(Candidate.id.asc()).paginate(page=page, per_page=pagination, error_out=False)
    # Serialize candidate data using the ResumeSchema schema
    resume_schema = CandidateSchema()
    datas = resume_schema.dump(query, many=True)
    # Determine if there is a next and/or previous page
    has_next, has_prev = int(query.has_next), int(query.has_prev)

    # Return serialized candidate data and pagination information wrapped in a dictionary
    return [datas, {'has_next': has_next, "has_prev": has_prev, 'title': title}]


@bp.get('/count')
@bp.doc(hide=True)  # APIFlask documentation decorator
@jwt_required()
def get_count():
    """
    Returns a JSON object containing the total number of candidates in the database with status NEWFAG and the number of 
    candidates that have not been FINISHed, RESULTed, or CANCELled and have a Check officer that is the current user.
    :return: A JSON object containing 'news' and 'checks' keys.
    :rtype: dict
    """
    news = db.session.query(func.count(Candidate.status)).filter(Candidate.status.in_([Status.NEWFAG.value,
                                                                                       Status.UPDATE.value])).scalar()
    messages = db.session.query(Message).filter(Message.status == Status.NEWFAG.value,
                                                Message.user_id == current_user.id).all()
    message_schema = MessageSchema()
    message = message_schema(messages, many=True) if messages else []
    return {'news': news if news is not None else 0,
            'counts': len(messages) if messages is not None else 0,
            'messages': message}


@bp.get('/reset')
@bp.doc(hide=True)  # Hide this endpoint from API documentation
@jwt_required()
def reset_count():
    """
    Reset the count of candidates.
    This function returns a JSON object containing the total number of candidates in the database with status NEWFAG and 
    the number of candidates that have not been FINISHed, RESULTed, or CANCELled and have a Check officer that is the 
    current user.
    :return: A JSON object containing 'counts' and 'messages' keys.
    :rtype: dict
    """
    # Update the status of all messages with status NEWFAG and current user id
    response = db.session.query(Message).filter(Message.status == Status.NEWFAG.value,
                                                Message.user_id == current_user.id).all()
    for resp in response:
        setattr(resp, 'status', Status.REPLY.value)
        db.session.commit()

    # Return the response with counts and an empty list of messages
    return {'counts': 0, 'messages': []}


@bp.post('/resume/create')
@bp.doc(hide=True)
@jwt_required()
def post_resume():
    """
    Create or update a candidate's resume based on the form data in the request.
    Returns:
        A dictionary with the candidate's ID and a message indicating if a new record was created or an existing one was updated
    """
    # Get the form data as a dictionary
    resume_dict: dict = request.get_json()
    # resume_dict: dict = request.get_json()
    # Query the database for a candidate with the same name and birthday
    result = db.session.query(Candidate).filter_by(fullname=resume_dict['fullname'],
                                                   birthday=resume_dict['birthday']).one_or_none()
    # Convert the birthday string to a datetime object
    resume_dict['birthday'] = datetime.strptime(resume_dict.pop('birthday'), "%Y-%m-%d")
    resume_dict['create'] = datetime.fromisoformat(resume_dict.pop('create'))
    if result:
        # If a candidate with the same name and birthday already exists, update their record
        resume_dict.update({'status': Status.UPDATE.value, 'update': TODAY})
        for k, v in resume_dict.items():
            setattr(result, k, v)
            db.session.commit()
        cand_id = result.id
        message = 'Запись уже существует. Данные обновлены'
    else:
        # If no candidate with the same name and birthday exists, create a new record
        resume_dict.update({'status': Status.NEWFAG.value, 'create': TODAY})
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
@jwt_required()
def get_profile(cand_id):
    """
    Returns the full profile of a candidate/employee based on the candidate ID
    """
    cand = db.session.query(Candidate).filter_by(id=cand_id).all()
    documents = db.session.query(Document).filter_by(cand_id=cand_id).order_by(Document.cand_id.asc()).all()
    address = db.session.query(Address).filter_by(cand_id=cand_id).order_by(Address.id.asc()).all()
    contacts = db.session.query(Contact).filter_by(cand_id=cand_id).order_by(Contact.id.asc()).all()
    workplaces = db.session.query(Workplace).filter_by(cand_id=cand_id).order_by(Workplace.id.asc()).all()
    staff = db.session.query(Staff).filter_by(cand_id=cand_id).order_by(Staff.id.asc()).all()
    checks = db.session.query(Check).filter_by(cand_id=cand_id).order_by(Check.id.asc()).all()
    registries = [db.session.query(Registry).filter(Registry.check_id == i.id).first() for i in checks]
    pfos = db.session.query(Poligraf).filter_by(cand_id=cand_id).order_by(Poligraf.id.asc()).all()
    invs = db.session.query(Investigation).filter_by(cand_id=cand_id).order_by(Investigation.id.asc()).all()
    inquiries = db.session.query(Inquiry).filter_by(cand_id=cand_id).order_by(Inquiry.id.asc()).all()
    
    resume_schema = CandidateSchema()
    staff_schema = StaffSchema()
    document_schema = DocumentSchema()
    address_schema = AddressSchema()
    contact_schema = ContactSchema()
    work_schema = WorkplaceSchema()
    check_schema = CheckSchema()
    registry_schema = RegistrySchema()
    poligraf_schema = PoligrafSchema()
    investigation_schema = InvestigationSchema()
    inquiry_schema = InquirySchema()
    # Return a list of dictionaries containing the candidate's information
    return [[resume_schema.dump(cand, many=True), 
             staff_schema.dump(staff, many=True),
             document_schema.dump(documents, many=True),
             address_schema.dump(address, many=True),
             contact_schema.dump(contacts, many=True),
             work_schema.dump(workplaces, many=True)],
             check_schema.dump(checks, many=True),
             registry_schema.dump(registries, many=True),
             poligraf_schema.dump(pfos, many=True),
             investigation_schema.dump(invs, many=True),
             inquiry_schema.dump(inquiries, many=True),
             {i.name: i.value for i in Status}]


@bp.post('/resume/upload')
@bp.doc(hide=True)
@jwt_required()
def upload_file():
    """
    Uploads a resume file and creates or updates a candidate record in the database

    Returns:
    A dictionary containing the candidate ID and a message indicating whether a new record was created or an existing
    record was updated
    """
    file = request.files['file']
    excel = ExcelFile(file)
    result = db.session.query(Candidate).filter(Candidate.fullname.ilike(excel.resume['fullname']),
                                                Candidate.birthday == (excel.resume['birthday'])).first()
    if result:  # If a record already exists, update it with the new data
        resum = excel.resume | {'status': Status.UPDATE.value, 'update': TODAY}
        for k, v in resum.items():
            setattr(result, k, v)
            db.session.commit()

        resume_data(result.id, excel.passport, excel.addresses, excel.contacts,
                    excel.workplaces, excel.staff)
        message = 'Запись уже существует. Данные обновлены'
    else:  # If no record exists, create a new one

        result = Candidate(**excel.resume | {'status': Status.NEWFAG.value, 'create': TODAY})
        db.session.add(result)
        db.session.flush()

        resume_data(result.id, excel.passport, excel.addresses, excel.contacts,
                    excel.workplaces, excel.staff)
        db.session.commit()
        message = 'Создана новая запись'
    return {'cand_id': result.id, 'message': message}


@bp.post('/update/<flag>/<cand_id>')
@bp.doc(hide=True)
@jwt_required()
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
    }
    model = model_map.get(flag)
    if not model:
        return {"message": "Возникла ошибка. Значение {}".format(flag.upper())}

    form_data: dict = request.get_json()

    # If updating documents convert the date string to a datetime object
    if flag == 'document':
        form_data['issue'] = datetime.strptime(form_data.pop('issue'), "%Y-%m-%d")

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
@jwt_required()
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
        docum = db.session.query(Document).filter_by(cand_id=cand_id).order_by(Document.id.desc()).first()
        addr = db.session.query(Address).filter_by(cand_id=cand_id).filter(Address.view.ilike("%регистрац%")). \
            order_by(Address.id.desc()).first()
        serial_resume, serial_docum, serial_addr  =  CandidateSchema(), DocumentSchema(), AddressSchema()
        serial = serial_resume.dump(resume) | serial_docum.dump(docum) | serial_addr.dump(addr)
        serial.update(officer=current_user.username)
        
        result = task_queue(serial)
        if result['message'] == "Success":
            db.session.add(Message(message=f'Анкета кандидата {resume.fullname} взята в работу',
                                    create=TODAY, user_id=current_user.id))
            resume.status = Status.ROBOT.value
            db.session.commit()
        elif result['message'] == "Fail":
            db.session.add(Message(message=f'Проверка кандидата {resume.fullname} не выполнена. Попробуйте позднее',
                                    create=TODAY, user_id=current_user.id))
            db.session.commit()
        else:
            db.session.add(Message(message=result['message'],
                                    create=TODAY, user_id=current_user.id))
            db.session.commit()
        return {'message': "Анкета поставлена в очередь"}
    else:
        # If the resume cannot be sent, return an error message
        return {'message': "Анкета не может быть отправлена. Проверка уже начата"}


@bp.get('/resume/status/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
def patch_status(cand_id: int) -> json:
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
        db.session.commit()
        return {"message": "Статус обновлен"}  # Return a success message
    else:
        return {"message": "Текущий статус обновить нельзя"}  # Return an error message


@bp.post('/check/<flag>/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
def post_check(flag: str, cand_id: int):
    candidate = db.session.query(Candidate).get(cand_id)
    try:
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
        # Get the data from the html form
        check_form: dict = request.get_json()
        check_form['deadline'] = datetime.strptime(check_form.pop('deadline'), "%Y-%m-%d")
        check_form['pfo'] = bool(check_form.pop('pfo')) if 'pfo' in check_form else False
        check_form = {k: (v if v else "Значимая информация не найдена") for k, v in check_form.items()}
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
    except Exception as e:
        candidate.status = Status.ERROR.value
        return {'message': f"Возникла ошибка: ({e})"}


@bp.get('/check/delete/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
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
    if candidate.status is not None and (candidate.status == Status.RESULT.value or candidate.status == Status.FINISH.value):
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
        return {'message': "Кандидат ещё не проверялся"}


@bp.get('/check/status/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
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
        alert = "alert-danger"
        message = "Анкета взята в работу и еще не закончена"
    else:
        # If the candidate's status is not being processed, set it to manual and commit changes to the database
        candidate.status = Status.MANUAL.value
        db.session.commit()
        alert = "alert-info"
        message = "Начата ручная проверка"

    # Return a JSON object containing the message to be displayed to the user
    return {'message': message, 'alert': alert}


@bp.post('/registry/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
def post_registry(cand_id):
    try:
        """Endpoint for posting a candidate's registry information"""
        form_registry = request.get_json()  # Load approval form
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
        response = requests.post(url='https://httpbin.org/post', json=json.dumps(
            {
                "id": candidate.request_id,
                "comments": reg['comments'],
                "decision": reg['decision'],
                "deadline": TODAY.strftime("%Y-%m-d%"),
                "supervisor": reg['supervisor']
            }
        ), timeout=5)
        response.raise_for_status()
        if response.status_code == 200:  # Check if the response was successfully sent
            candidate.status = Status.CANCEL.value if reg['decision'] == Status.CANCEL.value else Status.FINISH.value
            # Update candidate status based on decision
            db.session.commit()
            return {'message': "Решение успешно отправлено"}  # Return success message
        else:
            return {'message': 'Отправка не удалась попробуйте еще раз позднее'}  # Return failure message
    except Exception as e:
        return {"message": f"Ошибка добавления записи: {e}"}


@bp.post('/poligraf/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
def post_poligraf(cand_id):
    try:
        """
        View function that handles the Poligraf POST request for a candidate.
        Args:
            cand_id (int): The candidate ID.
        Returns:
            dict: A dictionary containing the message "Запись успешно добавлена".
        """
        # Retrieve the form data and convert the deadline string to a datetime object.
        form_poligraf: dict = request.get_json()
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
    except Exception as e:
        return {"message": f"Ошибка добавления записи: {e}"}


@bp.post('/investigation/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
def post_investigation(cand_id):
    try:
        """
        Adds a new investigation to the database for a given candidate.
        Args:
            cand_id (int): The ID of the candidate to add the investigation for.
        Returns:
            dict: A dictionary containing a success message.
        """
        # Get data from the form
        form_investigation: dict = request.get_json()

        # Convert the deadline string to a datetime object
        form_investigation['deadline'] = datetime.strptime(form_investigation.pop('deadline'), "%Y-%m-%d")

        # Add the investigation to the database
        db.session.add(Investigation(**form_investigation | {'cand_id': cand_id}))
        db.session.commit()
        # Return a success message
        return {"message": "Запись успешно добавлена"}
    except Exception as e:
        return {"message": f"Ошибка добавления записи: {e}"}


@bp.post('/inquiry/<int:cand_id>')
@bp.doc(hide=True)
@jwt_required()
def post_inquiry(cand_id):
    try:
        """
        This function handles a POST request to add an inquiry for a candidate.
        Args:
            cand_id (int): The ID of the candidate to add the inquiry for.
        Returns:
            dict: A dictionary containing a success message.
        """
        # Get the form data as a dictionary
        form_inquiry: dict = request.get_json()
        # Convert the 'deadline' string to a datetime object and update the form data
        form_inquiry['deadline'] = datetime.strptime(form_inquiry.pop('deadline'), "%Y-%m-%d")

        # Create a new Inquiry object with the form data and candidate ID, and add it to the database session
        db.session.add(Inquiry(**form_inquiry | {'cand_id': cand_id}))

        # Commit the changes to the database
        db.session.commit()

        # Return a success message
        return {"message": "Запись успешно добавлена"}
    except Exception as e:
        return {"message": f"Ошибка добавления записи: {e}"}


@bp.post('/information')
@bp.doc(hide=True)
@jwt_required()
def post_information():
    """
    Retrieve statistics for a given period of time.
    Returns:
        A dictionary containing candidate and poligraf statistics, as well as a title for the statistics.
    """
    # Retrieve data from the form submission
    period = request.get_json()
    # Retrieve candidate statistics from the database
    candidates = db.session.query(Registry.decision, func.count(Registry.id)).group_by(Registry.decision). \
        filter(Registry.deadline.between(period['start'], period['end'])).all()
    # Retrieve poligraf statistics from the database
    pfo = db.session.query(Poligraf.theme, func.count(Poligraf.id)).group_by(Poligraf.theme). \
        filter(Poligraf.deadline.between(period['start'], period['end'])).all()
    # Return a dictionary containing the candidate and poligraf statistics
    return {
        "candidates": dict(map(lambda x: (x[1], x[0]), candidates)),
        "poligraf": dict(map(lambda x: (x[1], x[0]), pfo))
        }


@bp.errorhandler(BadRequest)
def handle_bad_request(e):
    return 'bad request!', 400
