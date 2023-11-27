import random
import json

import requests
from faker import Faker

fake = Faker("ru-RU")


JSON_TEST = {
  "positionName": "Главный инженер по разработке",
  "department": "Группа разработки",
  "statusDate": "2023-10-23T11:14:24Z",
  "lastName": "Иванов",
  "firstName": "Иван",
  "midName": "Андреевич",
  "hasNameChanged": True,
  "nameWasChanged": [
    {
      "reason": "развод",
      "firstNameBeforeChange": "Петр",
      "lastNameBeforeChange": "Семенов",
      "hasNoMidNameBeforeChange": True,
      "yearOfChange": 2020,
      "nameChangeDocument": "документ"
    },
    {
      "reason": "усыновление/удочерение",
      "firstNameBeforeChange": "Степан",
      "lastNameBeforeChange": "Игоревич",
      "midNameBeforeChange": "Васильев",
      "yearOfChange": 2017,
      "nameChangeDocument": "документ 2"
    }
  ],
  "birthday": "1998-10-10",
  "birthplace": "Москва",
  "citizen": "Россия",
  "hasAdditionalCitizenship": True,
  "additionalCitizenship": "Австралия",
  "maritalStatus": "незарегистрированный брак",
  "regAddress": "Ленина 5",
  "validAddress": "Ленина 5",
  "contactPhone": "+70000000000",
  "hasNoRussianContactPhone": True,
  "email": "mail@pulse.com",
  "hasInn": True,
  "inn": "510189523890",
  "hasSnils": True,
  "snils": "36033751254",
  "passportSerial": "1234",
  "passportNumber": "566789",
  "passportIssueDate": "2015-05-10",
  "passportIssuedBy": "УФМС",
  "education": [
    {
      "educationType": "высшее",
      "institutionName": "МГУ",
      "beginYear": 2017,
      "endYear": 2020,
      "specialty": "менеджмент"
    },
    {
      "educationType": "MBA",
      "institutionName": "МГИМО",
      "beginYear": 2022,
      "endYear": 2023,
      "specialty": "экономика"
    }
  ],
  "hasJob": True,
  "experience": [
    {
      "beginDate": "1988-01-10",
      "endDate": "1989-01-10",
      "name": "ООО Мария",
      "address": "Ленина 1",
      "phone": "+70000000001",
      "activityType": "продажи",
      "position": "менеджер",
      "isPositionMatchEmploymentContract": True,
      "employmentContractPosition": "менеджер по продажам",
      "fireReason": "по собственному желанию"
    },
    {
      "beginDate": "1991-01-10",
      "currentJob": True,
      "name": "ПАО Александра",
      "address": "Ленина 9",
      "phone": "+70000000002",
      "activityType": "продажи",
      "position": "менеджер по обслуживанию"
    }
  ],
  "hasPublicOfficeOrganizations": True,
  "publicOfficeOrganizations": [
    {
      "name": "Учреждение А",
      "position": "стажер"
    },
    {
      "name": "Учреждение Б",
      "position": "методолог"
    }
  ],
  "hasStateOrganizations": True,
  "stateOrganizations": [
    {
      "name": " Министерство А",
      "position": "эксперт"
    },
    {
      "name": " Министерство Б",
      "position": "главный эксперт"
    }
  ],
  "hasRelatedPersonsOrganizations": True,
  "relatedPersonsOrganizations": [
    {
      "name": "Имя 1",
      "inn": "3171083718",
      "position": "специалист"
    },
    {
      "name": "Имя 2",
      "inn": "3171083718",
      "position": "ведущий специалист"
    }
  ],
  "hasMtsRelatedPersonsOrganizations": True,
  "mtsRelatedPersonsOrganizations": [
    {
      "name": "Имя 3"
    },
    {
      "name": "Имя 4"
    }
  ],
  "hasOrganizations": True,
  "organizations": [
    {
      "orgType": "самозанятость",
      "inn": "510189523890",
      "name": "ООО Смирнов",
      "workCombinationTime": "договор"
    },
    {
      "orgType": "ПАО",
      "inn": "3171083718",
      "name": "ОАО Иванов",
      "workCombinationTime": "договор"
    }
  ]
}


class AnketaTest:

    def __init__(self, request_id):
        self.request_id = request_id
        self.anketa = {
            "resume": {
                "id": str(request_id),
                "category": 'Кандидат',
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
                "department": f"Главный офис/{fake.company_suffix()}"
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

    def test_api_anketa(self, user, pswd):
        response = requests.post(f'{server}/api/v1/anketa',
                                 data=json.dumps(self.anketa),
                                 headers={'Content-Type': 'application/json'},
                                 auth=(user, pswd))
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

    def test_api_check(self, user, pswd, pers_id):
        self.check['id'] = pers_id
        response = requests.post(f'{server}/api/v1/check',
                                 data=json.dumps(self.check),
                                 headers={'Content-Type': 'application/json'},
                                 auth=(user, pswd))
        print(response.status_code)


if __name__ == '__main__':

    username = 'pulseapi'
    password = '88888888'
    server = 'http://127.0.0.1:5000'
    id_range = 2

    for person_id in range(1, id_range):
        anketa_test = AnketaTest(person_id)
        anketa_test.test_api_anketa(username, password)

    # for person_id in range(1, id_range):
    #     check_test = CheckTest()
    #     check_test.test_api_check(username, password, person_id)
