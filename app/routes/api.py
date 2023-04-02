import os
import shutil

import requests

from ..routes import bp
from ..extensions.extension import BASE_PATH, URL_CHECK, resume_data
from ..models.model import db, User, Candidate, Check, CheckSchema, SerialResume, \
    decerial_resume, TODAY, Status


# auth = HTTPBasicAuth()


# @auth.verify_password
def verify_password(username, password):
    if db.session.query(User).filter_by(username=username, password=password).first():
        return username
    return None


@bp.post('/api/v1/anketa')  # получение анкеты в формате JSON
@bp.input(SerialResume)
def anketa(resume):
    resume['resume']["request_id"] = resume['resume'].pop('id')  # удаляем id из анкеты и сохраняем  как request_id
    resume['resume']['status'] = Status.NEWFAG.value
    resume['resume']['deadline'] = TODAY
    candidate = db.session.query(Candidate).filter(Candidate.fullname.ilike(f"{resume['resume']['fullname']}"),
                                                   Candidate.birthday == resume['resume']['birthday']).first()
    if candidate:  # проверяем наличие такой же анкеты в БД, если уже есть
        for k, v in resume['resume'].items():  # перезаписываем анкету
            setattr(candidate, k, v)
            db.session.commit()
        new_id = candidate.id  # получаем id
    else:  # если нет - создаем новую запись
        value = Candidate(**resume['resume'])
        db.session.add(value)
        db.session.flush()
        new_id = int(value.id)  # получаем id
        db.session.commit()
    resume_data(new_id, resume['document'], resume['addresses'], resume['contacts'], resume['workplaces'],
                resume['staff'])  # записываем остальные данные в БД
    decerial = decerial_resume.decer_res(new_id, officer='API')
    response = requests.post(url=URL_CHECK, json=decerial, timeout=5)  # отправка анкеты на проверку
    response.raise_for_status()
    result = db.session.query(Candidate).filter_by(id=new_id).first()  # запрашиваем БД
    if response.status_code == 200:  # если отправка на проверку удалась
        result.status = Status.AUTO.value  # если отправка на проверку удалась ставим статус "Автомат"
        db.session.commit()
    else:
        if candidate:
            result.status = Status.UPDATE.value  # если отправка на проверку не удалась ставим статус "Новый"
            db.session.commit()
        else:
            result.status = Status.NEWFAG.value  # если отправка на проверку не удалась ставим статус "Новый"
            db.session.commit()
    return {"message": f'{resume}'}


@bp.post('/api/v1/check')  # получение результата проверки в формате JSON
@bp.input(CheckSchema)
def checkin(response):
    result = db.session.query(Candidate).filter_by(id=response['id']).first()
    if response['autostatus'] == Status.REPLY.value:
        result.status = Status.REPLY.value  # устанавливаем статус
        db.session.commit()
        path = os.path.join(BASE_PATH, result.fullname[0], f"{str(result.id)}-{result.fullname}",
                            TODAY.strftime("%Y-%m-%d"))
        # os.makedirs(path)  #  создаем папку для материалов проверки
        temp_path = response.pop('path', None)
        try:
            for file in os.listdir(temp_path):  # переносим файлы в новую папку
                print(file)
            #     shutil.copyfile(file, path)
        except FileNotFoundError as e:
            response['autostatus'] = f'{e}'
        response["cand_id"] = response.pop('id')  # удаляем id из проверки и заменяем на новый
        check_dict = response | {"path": path} | {"deadline": TODAY}
        db.session.add(Check(**check_dict))  # создаем новую запись
        db.session.commit()
    else:
        result.status = Status.ERROR.value  # устанавливаем статус
        db.session.commit()
    return {"message": f'{response}'}
