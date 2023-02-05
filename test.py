import json

import requests


def send_json(url, query):
    data = json.dumps(query)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url=url, data=data, headers=headers)
    response.raise_for_status()
    return response


query = '{ "staff": " ", "department": " ", "check_work_place": " ", "check_passport": "str",' \
        '"check_debt": "str", "check_bankruptcy": "str", "check_bki": "str", "check_affiliation": " ",' \
        '"check_terrorist": "str", "check_mvd": "str", "check_internet": " ", "check_cronos": " ",' \
        '"check_cross": " ", "check_addition": " ", "pfo": " ", "comment": " ", "resume": " ", "date_check": "str",' \
        '"officer": " ", "url": "str", "check_id": "6"}'

url = 'http://127.0.0.1:5000/api/v1/get_check'


send_json(url, query)
