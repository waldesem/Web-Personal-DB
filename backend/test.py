import random
import json

import requests
from faker import Faker

from app.models.classes import Category, Regions

fake = Faker("ru-RU")


class AnketaTest:

    def __init__(self):
        self.anketa = {
            "resume": {
                "id": str(random.randint(1, 999999)),
                "category": Category.candidate.value,
                "fullname": fake.name(),
                "previous": fake.last_name(),
                "birthday": fake.date_of_birth(minimum_age=14, 
                                            maximum_age=85).strftime("%Y-%m-%d"),
                "birthplace": fake.city(),
                "country": fake.country(),
                "snils": str(random.randint(10000000000, 99999999999)),
                "inn": fake.businesses_inn(),
                "education": fake.text(max_nb_chars=100),
            },
            "document": [{
                "view": fake.word(),
                "series": str(fake.random_int(min=1000, max=9999)),
                "number": str(fake.random_int(min=100000, max=999999)),
                "agency": fake.company(),
                "issue": fake.date_this_decade().strftime("%Y-%m-%d")
            }],
            "staff": [{
                "position": fake.job(),
                "department": f"{random.choice([region.value for region in Regions])}/{fake.company_suffix()}"
            }],
            "addresses": [
                {
                    "view": 'Адрес проживания',
                    "region": fake.region(),
                    "address": fake.address()
                },
                {
                    "view": 'Адрес регистрации',
                    "region": fake.region(),
                    "address": fake.address()
                }
            ],
            "workplaces": [
                {
                    'start_date': fake.date_this_decade().strftime("%Y-%m-%d"),
                    'end_date': fake.date_this_decade().strftime("%Y-%m-%d"),
                    "workplace": fake.company(),
                    "address": fake.address(),
                    "position": fake.job()
                },
                {
                    'start_date': fake.date_this_decade().strftime("%Y-%m-%d"),
                    'end_date': fake.date_this_decade().strftime("%Y-%m-%d"),                
                    "workplace": fake.company(),
                    "address": fake.address(),
                    "position": fake.job()
                },
                {
                    'start_date': fake.date_this_decade().strftime("%Y-%m-%d"),
                    'end_date': fake.date_this_decade().strftime("%Y-%m-%d"),                
                    "workplace": fake.company(),
                    "address": fake.address(),
                    "position": fake.job()
                }
            ],
            "contacts": [
                {
                    "view": 'Номер телефона',
                    "contact": fake.phone_number()
                },
                {
                    "view": 'Электронная почта',
                    "contact": fake.email()
                }
            ]
        }


    def test_api_anketa(self, user, paswd):
        response = requests.post(f'{server}/api/v1/anketa', 
                                 data=json.dumps(self.anketa), 
                                 headers={'Content-Type': 'application/json'},
                                 auth=(user, paswd))
        print(response.status_code)


class CheckTest:
    
    def __init__(self) -> None:
        self.check = {
            'id': '',
            'employee': fake.text(max_nb_chars=100),
            'document': fake.text(max_nb_chars=100),
            'inn': fake.text(max_nb_chars=100),
            'debt': fake.text(max_nb_chars=100),
            'bankruptcy': fake.text(max_nb_chars=100),
            'bki': fake.text(max_nb_chars=100),
            'courts': fake.text(max_nb_chars=100),
            'affiliation': fake.text(max_nb_chars=100),
            'terrorist': fake.text(max_nb_chars=100),
            'mvd': fake.text(max_nb_chars=100),
            'path': ''
        }

    def test_api_check(self, user, paswd, person_id):
        self.check['id'] =  person_id
        response = requests.post(f'{server}/api/v1/check', 
                                 data=json.dumps(self.check), 
                                 headers={'Content-Type': 'application/json'}, 
                                 auth=(user, paswd))
        print(response.status_code)


if __name__ == '__main__':

    username='pulseapi'
    password='88888888'
    server='http://127.0.0.1:5000'

    for _ in range(10):
        anketa_test = AnketaTest()
        anketa_test.test_api_anketa(username, password)

    id_list = []
    for person_id in id_list:
        check_test = CheckTest()
        check_test.test_api_check(username, password, person_id)

