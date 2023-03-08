import os
import shutil
import json
from datetime import datetime

import requests
from flask import request, jsonify
from marshmallow import ValidationError

# from flask_httpauth import HTTPBasicAuth

from . import bpa
from ..utils.extensions import STATUS, BASE_PATH, TODAY, resume_data, URL_CHECK
from ..models.model import db, User, Candidate, Check, resume_schema, check_schema


# auth = HTTPBasicAuth()


# @auth.verify_password
def verify_password(username, password):
    if db.session.query(User).filter_by(username=username, password=password).first():
        return username
    return None


@bpa.route('/api/v1/anketa', methods=['POST'])  # получение анкеты в формате JSON
# @auth.login_required
def anketa():
    print(request.get_json())
    try:
        resume = resume_schema.loads(request.data)
        print(resume)
        return jsonify({'status': 'success'})

        # birth = datetime.strptime(resume['resume']['birthday'], "%Y-%m-%d").date()  # получаем даты в формате datatime
        # issue = datetime.strptime(resume['document']['issue'], "%Y-%m-%d").date()
        # resume['resume']['birthday'] = birth  # сохраняем даты в новом формате
        # resume['document']['issue'] = issue  # собираем предварительные данные для записи в БД
        # resume["request_id"] = resume.pop('id')  # удаляем id из анкеты и сохраняем его как request_id
        # add_resume = {'status': f'{STATUS["autocheck"]} A'} | {"deadline": TODAY}
        # result = db.session.query(Candidate).filter_by(fullname=resume['resume']['fullname'], birthday=birth).first()
        # if result:  # проверяем наличие такой же анкеты в БД, если уже есть
        #     for k, v in resume['resume'] | add_resume.items():  # перезаписываем анкету
        #         setattr(result, k, v)
        #         db.session.commit()
        #     new_id = result.id  # получаем id
        #     resume_data(new_id, resume['document'], resume['address'], resume['contact'], resume['work'], resume['staff'])
        #     response = requests.post(url=URL_CHECK, json=resume | {'id': new_id} | add_resume | {'officer': 'API'})
        # else:  # если нет - создаем новую запись
        #     value = Candidate(**resume['resume'] | add_resume)
        #     db.session.add(value)
        #     db.session.flush()
        #     new_id = int(value.id)  # получаем id
        #     print(type(new_id))
        #     resume_data(new_id, resume['document'], resume['address'], resume['contact'], resume['work'], resume['staff'])
        #     db.session.commit()
        #     response = requests.post(url=URL_CHECK, json=jsonify(resume | {'id': new_id} | add_resume | {'officer': 'API'}))
        # response.raise_for_status()
        # if response.status_code != 200 or response.status_code != 201:  # если отправка на проверку не удалась
        #     result = db.session.query(Candidate).filter_by(id=new_id).first()  # запрашиваем БД
        #     result.status = STATUS['new']
        #     db.session.commit()
        # return jsonify({"status": "successful"})

    except ValidationError as error:
        return jsonify({"status": error})


@bpa.route('/api/v1/check', methods=['POST'])  # получение результата проверки в формате JSON
# @auth.login_required
def check():
    try:
        response = check_schema.loads(request.data)
        result = db.session.query(Candidate).filter_by(id=response['id']).first()
        result.status = STATUS['robotend']  # устанавливаем статус Предварительно
        db.session.commit()
        path = os.path.join(BASE_PATH, result.fullname[0], f"{str(result.id)}-{result.fullname}",
                            TODAY.strftime("%Y-%m-%d"))
        # os.makedirs(path)  #  создаем папку для материалов проверки
        temp_path = response.pop("path", None)
        # for file in os.listdir(temp_path):  # переносим файлы в новую папку
        #     shutil.copyfile(file, path)
        response["cand_id"] = response.pop('id')  # удаляем id из проверки и заменяем на новый
        check_dict = response | {"path": path} | {"deadline": TODAY}
        db.session.add(Check(**check_dict))  # создаем новую запись
        db.session.commit()
        return jsonify({"status": "success"})
    except ValidationError as error:
        return jsonify({"status": error})
