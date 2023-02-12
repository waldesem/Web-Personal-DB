import json
import os
import shutil

from sqlalchemy import func
from flask import request, abort, jsonify, Markup, flash
import requests

from . import bpa
from app.models.model import *

STATUS = dict(new='Новый', active='Начато', robot_start='Автопроверка', robot_end='Предварительно',
              finish='Закончено', pfo_start='ПФО', result='Решение')  # статусы проверки кандидата


@bpa.route('/api/v1/get_resume', methods=['POST'])  # получение анкеты в формате JSON
def get_resume():
    if not request.json:
        abort(400)
    else:  # валидация данных
        response = request.get_json()
        resume = json.loads(response)
        if response:
            result = db.session.query(Candidate).filter(func.lower(Candidate.full_name == resume['full_name'].lower()),
                                                        func.lower(
                                                            Candidate.birthday == resume['birthday'].lower())).first()
            if result is None:  # проверяем есть такой кандидат в БД или нет
                db.session.add(Candidate(**resume))  # если нет - создаем новую запись
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
            return jsonify({'get_status': f'not vallid json data{str(response)}'}), 406


@bpa.route('/api/v1/get_check', methods=['POST'])  # получение результата проверки в формате JSON
def get_check():
    if not request.json:
        abort(400)
    else:  # валидация данных
        response = request.get_json()
        check = json.loads(response)
        if response:
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
            return jsonify('{"get_status": "not vallid json data "'f'{response}''"}'), 406


@bpa.route('/api/v1/send_resume/<int:cand_id>', methods=['GET'])  # отправка анкеты на проверку
def send_resume(cand_id, mark=True):  # mark - флаг для обозначения автомат отправил анкету или вручную
    result = db.session.query(Candidate).filter_by(id=cand_id).first()
    decer = cand_schema.dump(result)  # десериализация результата запроса
    url = "http://localhost:5000/api/v1/send_resume"  # адрес для отправки анкеты на проверку
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url=url, data=json.dumps(decer), headers=headers, timeout=5)
    response.raise_for_status()
    if response.json():
        if mark:
            flash(Markup("Анкета успешно отправлена"))
        else:
            pass  # отправитьь на почту сообщение об ошибке
        result.status = STATUS['robot_start']  # устанавливаем статус Автопроверка
        db.session.commit()
    else:
        if mark:
            flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"))


@bpa.route('/api/v1/send_registr/<int:cand_id>', methods=['GET'])  # отправка анкеты на проверку
def send_registr(candidate, reg):
    url = "http://localhost:5000/api/v1/send_registr"  # адрес для отправки ответа по результам проверки
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    value = {'id': candidate.request_id, 'marks': reg['marks'], 'decision': reg['decision'],
             'date': reg['dec_date'], 'supervisor': reg['supervisor']}
    response = requests.post(url=url, data=json.dumps(value), headers=headers, timeout=5)
    response.raise_for_status()
