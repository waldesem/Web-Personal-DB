import os
import shutil

import requests
from flask import request, jsonify
from marshmallow import ValidationError

# from flask_httpauth import HTTPBasicAuth

from . import bpa
from ..utils.extensions import BASE_PATH, TODAY, resume_data, URL_CHECK
from ..models.model import db, User, Candidate, Check, check_schema, candidate_schema, decerial_resume, ErrorLog
from ..forms.form import STATUS

# auth = HTTPBasicAuth()


# @auth.verify_password
def verify_password(username, password):
    if db.session.query(User).filter_by(username=username, password=password).first():
        return username
    return None


@bpa.route('/api/v1/anketa', methods=['POST'])  # получение анкеты в формате JSON
# @auth.login_required
def anketa():
    json_data = request.data
    if not json_data:
        return {"message": "No input data provided"}, 400
    try:
        resume = candidate_schema.loads(json_data)
        resume['resume']["request_id"] = resume['resume'].pop('id')  # удаляем id из анкеты и сохраняем  как request_id
        resume['resume']['status'] = STATUS["autocheck"]
        resume['resume']['deadline'] = TODAY
        result = db.session.query(Candidate).filter_by(fullname=resume['resume']['fullname'],
                                                       birthday=resume['resume']['birthday']).first()
        if result:  # проверяем наличие такой же анкеты в БД, если уже есть
            for k, v in resume['resume'].items():  # перезаписываем анкету
                setattr(result, k, v)
                db.session.commit()
            new_id = result.id  # получаем id
        else:  # если нет - создаем новую запись
            value = Candidate(**resume['resume'])
            db.session.add(value)
            db.session.flush()
            new_id = int(value.id)  # получаем id
            db.session.commit()
        resume_data(new_id, resume['document'], resume['addresses'], resume['contacts'], resume['workplaces'],
                    resume['staff'])    # записываем остальные данные в БД
        decerial = decerial_resume.decer_res(new_id, officer='API')
        response = requests.post(url=URL_CHECK, json=decerial, timeout=5)  # отправка анкеты на проверку
        response.raise_for_status()
        if response.status_code == 200:  # если отправка на проверку удалась
            return jsonify({"status": "Automatic processing"})
        else:
            result = db.session.query(Candidate).filter_by(id=new_id).first()  # запрашиваем БД
            result.status = STATUS['new']   # если отправка на проверку не удалась ставим статус "Новый"
            db.session.commit()
            return jsonify({"status": "Рartially successful. Manual processing"})
    except ValidationError as error:
        db.session.add(ErrorLog(**{"resume_error": error, "deadline": TODAY}))
        db.session.flush()
        return jsonify({"status": error})


@bpa.route('/api/v1/check', methods=['POST'])  # получение результата проверки в формате JSON
# @auth.login_required
def check():
    json_data = request.data
    if not json_data:
        return {"message": "No input data provided"}, 400
    try:
        response = check_schema.loads(json_data)
        result = db.session.query(Candidate).filter_by(id=response['id']).first()
        result.status = STATUS['autoend']  # устанавливаем статус Автовозврат
        db.session.commit()
        path = os.path.join(BASE_PATH, result.fullname[0], f"{str(result.id)}-{result.fullname}",
                            TODAY.strftime("%Y-%m-%d"))
        # os.makedirs(path)  #  создаем папку для материалов проверки
        temp_path = response.pop(path, None)
        for file in os.listdir(temp_path):  # переносим файлы в новую папку
            print(file)
        #     shutil.copyfile(file, path)
        response["cand_id"] = response.pop('id')  # удаляем id из проверки и заменяем на новый
        check_dict = response | {"path": path} | {"deadline": TODAY}
        db.session.add(Check(**check_dict))  # создаем новую запись
        db.session.commit()
        return jsonify({"status": "success"})
    except ValidationError as error:
        db.session.add(ErrorLog(**{"check_error": error, "deadline": TODAY}))
        db.session.flush()
        return jsonify({"status": error})
