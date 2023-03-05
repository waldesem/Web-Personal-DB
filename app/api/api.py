import os
import shutil
import json

from flask import request, jsonify
# from flask_httpauth import HTTPBasicAuth

from . import bpa
from ..utils.extensions import *


# auth = HTTPBasicAuth()


# @auth.verify_password
def verify_password(username, password):
    if db.session.query(User).filter_by(username=username, password=password).first():
        return username
    return None


@bpa.route('/api/v1/anketa', methods=['POST'])  # получение анкеты в формате JSON
# @auth.login_required
def anketa():
    resume = json.loads(request.data)
    if resume['resume']['fullname'] and resume['resume']['birthday']:
        result = db.session.query(Candidate).filter(Candidate.fullname == resume['resume']['fullname'],
                                                    (Candidate.birthday == resume['resume']['birthday'])).first()
        resume["request_id"] = resume.pop('id')  # удаляем id из анкеты и заменяем на новый
        birth = resume['resume']['birthday']
        issue = resume['document']['issue']
        resume['resume']['birthday'] = datetime.strptime(birth, "%Y-%m-%d").date()
        resume['document']['issue'] = datetime.strptime(issue, "%Y-%m-%d").date()
        res = resume['resume'] | {'status': STATUS['new']} | {"deadline": TODAY}
        print(res)
        if result:  # проверяем наличие такой же анкеты в БД
            for k, v in res.items():
                setattr(result, k, v)  # перезаписываем анкету
                db.session.commit()
            resume_data(result.id, resume['document'], resume['address'],
                        resume['contact'], resume['work'], resume['staff'])
        else:  # если нет - создаем новую запись
            value = Candidate(**res)
            db.session.add(value)
            db.session.flush()
            resume_data(value.id, resume['document'], resume['address'],
                        resume['contact'], resume['work'], resume['staff'])
            db.session.commit()
        return jsonify({"status": "successful"})
    else:
        return jsonify({"status": "error"})


@bpa.route('/api/v1/check', methods=['POST'])  # получение результата проверки в формате JSON
# @auth.login_required
def check():
    response = json.loads(request.data)
    if response['id']:
        result = db.session.query(Candidate).filter_by(id=response['id']).first()
        result.status = STATUS['robot_end']  # устанавливаем статус Предварительно
        db.session.commit()
        path = os.path.join(BASE_PATH, result.fullname[0], f"{str(result.id)}-{result.fullname}",
                            TODAY.strftime("%Y-%m-%d"))
        # os.makedirs(path)  #  создаем папку для материалов проверки
        # temp_path = response.pop("temp_path", None)
        # for file in os.listdir(temp_path):  # переносим файлы в новую папку
        #     shutil.copyfile(file, path)
        response["cand_id"] = response.pop('id')  # удаляем id из проверки и заменяем на новый
        response.pop('temp_path', None)
        check_dict = response | {"path": path} | {"deadline": TODAY}
        db.session.add(Check(**check_dict))  # создаем новую запись
        db.session.commit()
        return jsonify({"status": "successful"})
    else:
        return jsonify('{"status": "error"}')
