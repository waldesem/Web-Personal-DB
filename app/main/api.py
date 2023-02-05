import json
import os
import shutil

from flask import request, abort, jsonify, Markup, flash, make_response

from . import bp_api
from app.models.model import *
from app.pydantic.validate import *
from ..utils.extensions import send_json, create_folder, STATUS


@bp_api.route('/api/v1/get_resume', methods=['POST'])  # получение анкеты в формате JSON
def get_resume():
    if not request.json:
        abort(400)
    else:  # валидация данных
        response = request.get_json()
        resume = json.loads(response)
        resp = validate_resume(resume)
        if resp:
            result = db.session.query(Candidate).filter_by(full_name=resume['full_name'],
                                                           birthday=resume['birthday']).first()
            if result is None:  # проверяем есть такой кандидат в БД или нет
                db.session.add(Candidate(**resume))     # если нет - создаем новую запись
                db.session.commit()
            else:
                for k, v in resume.items():  # если да, то перезаписываем анкету
                    setattr(result, k, v)
                    db.session.commit()
            result = db.session.query(Candidate).filter_by(full_name=resume['full_name'],
                                                           birthday=resume['birthday']).first()
            result.status = STATUS['new']  # устанавливаем статус новая анкета
            db.session.commit()
            # send_resume(result.id, mark=False)  # mark - флаг что анкета поступила автоматическая
            return jsonify({'get_status': 'successful'}), 201
        else:
            return jsonify({'get_status': f'not vallid json data{str(resp)}'}), 406


@bp_api.route('/api/v1/get_check', methods=['POST'])  # получение результата проверки в формате JSON
def get_check():
    if not request.json:
        abort(400)
    else:  # валидация данных
        response = request.get_json()
        check = json.loads(response)
        resp = validate_check(check)
        if resp:
            value = Check(**check)  # создаем новую запись
            db.session.add(value)
            db.session.commit()
            result = db.session.query(Candidate).filter_by(id=check['check_id']).first()
            result.status = STATUS['robot_end']  # устанавливаем статус Предварительно
            # folder = create_folder(result.full_name)
            # for file in os.listdir('/robot/check/path'):
            #     shutil.copyfile(file, folder)
            return jsonify('{"get_status": "successful"}'), 201
        else:
            return jsonify('{"get_status": "not vallid json data "'f'{resp}''"}'), 406


@bp_api.route('/api/v1/send_resume/<int:cand_id>', methods=['GET'])  # отправка анкеты на проверку
def send_resume(cand_id, mark=True):  # mark - флаг для обозначения автомат отправил анкету или вручную
    result = db.session.query(Candidate).filter_by(id=cand_id).first()
    dictret = result.__dict__
    url = "http://localhost:5000/api/v1/get_resume"  # адрес для отправки анкеты на проверку
    resp = send_json(url, json.dumps(dictret))  # отправка запроса
    if resp.json()['request'] == 'successful':
        if mark:
            flash(Markup("Анкета успешно отправлена"))
        else:
            pass  # отправитьь на почту сообщение об ошибке
        result.status = STATUS['robot_start']  # устанавливаем статус Автопроверка
        db.session.commit()
    else:
        if mark:
            flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"))


@bp_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}))
