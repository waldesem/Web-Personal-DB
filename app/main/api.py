import json
import os
from datetime import date
from getpass import getuser

import requests
from flask import request, abort, jsonify, Markup, flash

from app.models.model import *
from . import bp_api

TODAY = date.today().strftime('%Y-%m-%d')
STATUS = dict(new='Новый кандидат',
              active='Проверка начата',
              robot_start='Автопроверка',
              robot_end='Автопроверка окончена',
              finish='Проверка окончена',
              pfo_start='Назначено ПФО',
              pfo_end='ПФО проведено',
              result='Решение принято')     # статусы проверки кандидата


@bp_api.route('/api/v1/get_resume/', methods=('GET', 'POST'))  # получение анкеты в формате JSON
def get_resume(take_resume):
    if not request.json or 'title' not in request.json:
        abort(400)
    else:
        resume = json.loads(take_resume)
        result = db.session.query(Candidate).select_from(Candidate).filter_by(full_name=resume['full_name'],
                                                                              birthday=resume['birthday']).first()
        if result is not None:  # проверяем есть такой кандидат в БД или нет
            for k, v in resume.items():     # если да, то перезаписываем анкету
                setattr(result, k, v)
                db.session.commit()
        else:
            value = Candidate(**resume)     # если нет - создаем новую запись
            db.session.add(value)
            db.session.commit()
        setattr(result, result.status, STATUS['new'])    # устанавливаем статус новая анкета
        return jsonify({'request': 'successful'}), 201


@bp_api.route('/api/v1/get_check/<url>', methods=('GET', 'POST'))     # получение результата в формате JSON
def get_check(url):
    if not request.json or 'title' not in request.json:
        abort(400)
    else:   # получаем JSON с результатом проверки, берем из него ID
        check = json.loads(url)
        result = db.session.query(Candidate).select_from(Candidate).filter_by(full_name=check['full_name'],
                                                                              birthday=check['birthday']).first()
        check['check_id'] = result.id
        check_res = db.session.query(Check).select_from(Check).filter_by(id=check['id']).first()
        for k, v in check.items():
            if v is not '':      # записываем данные проверки
                setattr(check_res, k, v)
                db.session.commit()
        setattr(result, result.status, STATUS['robot_end'])    # устанавливаем статус Автопроверка окончена
        return jsonify({'request': 'successful'}), 201


@bp_api.route('/api/v1/send_resume/<int:cand_id>', methods=('GET', 'POST'))
def send_resume(cand_id):
    result = db.session.query(Candidate).select_from(Candidate).filter_by(id=cand_id).first()
    url = "http://localhost:8080"
    data = jsonify(result)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    resp = requests.post(url=url, data=data, headers=headers)
    resp.raise_for_status()
    if json.loads(resp.json())['request'] == 'successful':
        message = Markup("Анкета успешно отправлена")
        flash(message)
        setattr(result, result.status, STATUS['robot_start'])    # устанавливаем статус Автопроверка
        url = rf'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-2\{result.full_name[0]}\
                            \{result.id} - {result.full_name}'
        os.mkdir(os.path.join(url, TODAY))  # создаем папку для хранения анкет и материалов проверки
        start_check = Check()
        start_check.officer = getuser()
        start_check.url = url
        start_check.date_check = TODAY
        db.session.add(Check(start_check))
        db.session.commit()     # формируем черновую запись проверки, записываем в БД путь, дату и сотрудника СБ
    else:
        message = Markup("Отправка анкеты не удалась попробуйте ещее раз позднее")
        flash(message)
