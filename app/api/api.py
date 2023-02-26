import os
import shutil

from flask import request, jsonify

from . import bpa
from ..utils.extensions import *


@bpa.route('/api/anketa', methods=['GET', 'POST'])  # получение анкеты в формате JSON
def anketa():
    resume = request.get_json()
    if resume['resume']['full_name'] and resume['resume']['birthday']:
        result = db.session.query(Candidate).filter(Candidate.full_name == resume['resume']['full_name'],
                                                    (Candidate.birthday == resume['resume']['birthday'])).first()
        resume["request_id"] = resume.pop('id')  # удаляем id из анкеты и заменяем на новый
        res = resume['resume'] | {'status': STATUS['new']} | {"update_date": datetime.now().strftime('%Y-%m-%d %H:%M')}
        if result:  # проверяем наличие такой же анкеты в БД
            for k, v in res.items():
                setattr(result, k, v)  # перезаписываем анкету
                db.session.commit()
            resume_data(result.id, resume['passport'], resume['address'],
                        resume['contact'], resume['work'], resume['staff'])
        else:  # если нет - создаем новую запись
            value = Candidate(**res)
            db.session.add(value)
            db.session.flush()
            resume_data(value.id, resume['passport'], resume['address'],
                        resume['contact'], resume['work'], resume['staff'])
            db.session.commit()
        return jsonify({"get_status": "successful"}), 201
    else:
        return jsonify({"get_status": "error"}), 400


@bpa.route('/api/check', methods=['GET', 'POST'])  # получение результата проверки в формате JSON
def check():
    response = request.get_json()
    if response['id']:
        result = db.session.query(Candidate).filter_by(id=response['id']).first()
        result.status = STATUS['robot_end']  # устанавливаем статус Предварительно
        db.session.commit()
        path = os.path.join(BASE_PATH, result.full_name[0], f"{str(result.id)}-{result.full_name}",
                            datetime.now().strftime('%Y-%m-%d'))
        # os.makedirs(path)  #  создаем папку для материалов проверки
        # temp_path = response.pop("temp_path", None)
        # for file in os.listdir(temp_path):  # переносим файлы в новую папку
        #     shutil.copyfile(file, path)
        response["check_id"] = response.pop('id')  # удаляем id из проверки и заменяем на новый
        check_dict = response | {"path": path}
        db.session.add(Check(**check_dict))  # создаем новую запись
        db.session.commit()
        return jsonify({"get_status": "successful"}), 201
    else:
        return jsonify('{"get_status": "error"}'), 406
