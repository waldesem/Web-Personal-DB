import json
import os
import shutil
from datetime import datetime

from flask import request, jsonify, Markup, flash, url_for, redirect
import requests

from . import bpa
from app.models.model import *
from ..utils.extensions import STATUS, resume_data


@bpa.route('/api/v1/get_resume', methods=['POST'])  # получение анкеты в формате JSON
def get_resume():
    resume = request.get_json()
    if resume:  # проверяем наличие такой же анкеты в БД
        result = db.session.query(Candidate).filter(Candidate.full_name == resume['resume']['full_name'],
                                                    (Candidate.birthday == resume['resume']['birthday'])).first()
        res = resume['resume'] | {'status': STATUS['new']} | {"update_date": datetime.now().strftime('%Y-%m-%d %H:%M')}
        if result:  # если есть устанавливаем статус, дату и обновляем данные
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


@bpa.route('/api/v1/get_check', methods=['POST'])  # получение результата проверки в формате JSON
def get_check():
    response = request.get_json()
    if response:
        result = db.session.query(Candidate).filter_by(id=response['check_id']).first()
        result.status = STATUS['robot_end']  # устанавливаем статус Предварительно
        db.session.commit()
        path = os.path.join(rf'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-2\\',
                            result.full_name[0], f"{str(result.id)} - {result.full_name}",
                            datetime.now().strftime('%Y-%m-%d_%H-%M'))
        # os.makedirs(path)  #  создаем папку для материалов проверки
        temp_path = response.pop("temp_path", None)
        check_dict = response | {"path": path}
        db.session.add(Check(**check_dict))  # создаем новую запись
        db.session.commit()
        for file in os.listdir(temp_path):
            print(file)
        #     shutil.copyfile(file, path)
        return jsonify({"get_status": "successful"}), 201
    else:
        return jsonify('{"get_status": "error"}'), 406


@bpa.route('/api/v1/send_resume/<int:cand_id>', methods=['GET'])  # отправка анкеты на проверку
def send_resume(cand_id):
    candidate = db.session.query(Candidate).filter_by(id=cand_id).first()
    passport = db.session.query(Passport).filter_by(passport_id=cand_id).order_by(Passport.passport_id.desc()).first()
    address = db.session.query(Address).filter_by(address_id=cand_id). \
        filter(Address.type.ilike("%регистрац%")).order_by(Address.address_id.desc()).first()
    cand, passp, addr = cand_schema.dump(candidate), passp_schema.dump(passport), addr_schema.dump(address)
    decer = {"resume": cand} | {"passport": passp} | {"address": addr}  # десериализация и merge результатов запроса
    url = "https://httpbin.org/post"  # адрес для отправки анкеты на проверку
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url=url, data=json.dumps(decer), headers=headers, timeout=1)
    response.raise_for_status()
    if response.status_code == 200:
        flash(Markup("Анкета успешно отправлена"))
        candidate.status = STATUS['robot_start']  # устанавливаем статус Автопроверка
        db.session.commit()
        return redirect(url_for('route.index'))
    else:
        flash(Markup("Отправка анкеты не удалась попробуйте еще раз позднее"))
        return redirect(url_for('route.profile', cand_id=cand_id))


@bpa.route('/api/v1/send_registr/<int:cand_id>', methods=['GET'])  # отправка согласования
def send_registr(candidate, reg):
    url = "https://httpbin.org/post"  # адрес для отправки ответа по результам проверки
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    value = {"id": candidate.request_id, "marks": reg['marks'], "decision": reg['decision'],
             "date": reg['dec_date'], "supervisor": reg['supervisor']}
    response = requests.post(url=url, data=json.dumps(value), headers=headers, timeout=1)
    response.raise_for_status()
    return response
