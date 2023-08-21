import random
from faker import Faker
import requests
import json
from app.models.classify import Category, regions

fake = Faker("ru-RU")

def get_anketa(index):
    return [{
        "resume": {
            "id": i,
            "category": random.choice([category.value for category in Category]),
            "fullname": fake.name(),
            "previous": fake.last_name(),
            "birthday": fake.date_of_birth(minimum_age=18, maximum_age=95).strftime("%Y-%m-%d"),
            "birthplace": fake.city(),
            "country": fake.country(),
            "snils": fake.ssn(),
            "inn": fake.businesses_inn(),
            "education": fake.text(max_nb_chars=100),
        },
        "document": {
            "view": fake.word(),
            "series": str(fake.random_int(min=1000, max=9999)),
            "number": str(fake.random_int(min=100000, max=999999)),
            "agency": fake.company(),
            "issue": fake.date_this_decade().strftime("%Y-%m-%d")
        },
        "staff": {
            "position": fake.job(),
            "department": f'{random.choice(regions)}/{fake.company_suffix()}'
        },
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
    } for i in index]


def test_api(number=20, server='http://127.0.0.1:5000', username='newapi', password = 'newapi'):
    anketas = get_anketa(number)
    for anketa in anketas:
        response = requests.post(f'{server}/api/v1/anketa', 
                                data=json.dumps(anketa), 
                                headers={
                                    'Content-Type': 'application/json'
                                    }, 
                                auth=(username, password))
        if response.status_code == 200:
            print(response.status_code)
        else:
            print(response.text)


if __name__ == '__main__':
    test_api()