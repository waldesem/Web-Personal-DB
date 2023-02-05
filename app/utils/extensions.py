import os
from datetime import date

import requests
from flask import jsonify, url_for


TODAY = date.today().strftime('%Y-%m-%d')
STATUS = dict(new='Новый', active='Начато', robot_start='Автопроверка', robot_end='Предварительно',
              finish='Закончено', pfo_start='ПФО', result='Решение')  # статусы проверки кандидата


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


def send_json(url, query):
    data = jsonify(query)
    # return jsonify({'tasks': map(make_public_task, tasks)})
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url=url, data=data, headers=headers)
    response.raise_for_status()
    return response


def create_folder(name):  # создаем папку для хранения анкет и материалов проверки
    # url = os.path.join(rf'\\cronosx1\New folder\УВБ\Отдел корпоративной защиты\Персонал\Персонал-2\{name.full_name[0]}\
    #                 \{name.id} - {name.full_name}', TODAY)
    url = os.path.join(rf'/home/semenenko/MyProjects/', name.full_name[0], f'{str(name.id)} - {name.full_name}', TODAY)
    os.makedirs(url)
    return url
