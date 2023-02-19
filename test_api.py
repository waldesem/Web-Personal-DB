import requests
from faker import Faker
from flask import jsonify

fake = Faker()

RESUME = dict(region=fake.city(),
              full_name=fake.name(),
              last_name=fake.name(),
              birthday=fake.date(),
              birth_place=fake.city(),
              country=fake.country(),
              series_passport=fake.random_number(digits=4),
              number_passport=fake.random_number(digits=6),
              agency=fake.company(),
              date_given=fake.date(),
              snils=fake.random_number(digits=12),
              inn=fake.random_number(digits=12),
              reg_address=fake.address(),
              live_address=fake.address(),
              phone=fake.phone_number(),
              email=fake.email(),
              education=fake.text(),
              workplace_1=fake.company(),
              workplace_2=fake.company(),
              workplace_3=fake.company(),
              addition="",
              update_date=fake.date(),
              status="",
              request_id=fake.random_number(digits=5)
              )

CHECK = dict(staff="",
             department="",
             former_employee=fake.text(),
             check_work_place="",
             check_passport=fake.text(),
             check_inn=fake.text(),
             check_debt=fake.text(),
             check_bankruptcy=fake.text(),
             check_bki=fake.text(),
             check_court=fake.text(),
             check_affiliation=fake.text(),
             check_terrorist=fake.text(),
             check_mvd=fake.text(),
             check_internet="",
             check_cronos="",
             check_cross="",
             check_addition="",
             pfo="",
             comment="",
             resume="",
             date_check="",
             officer="",
             url=fake.url()
             )

REGISTR = dict(marks=fake.text(),
               decision=fake.text(),
               dec_date=fake.date(),
               supervisor=fake.name(),
               registr_cand_id=fake.random_number(digits=5)
               )

URL_RES_GET = 'http://127.0.0.1:5000/api/v1/get_resume'
URL_CH_GET = 'http://127.0.0.1:5000/api/v1/get_check'
URL_CH_SEND = "http://localhost:5000/api/v1/send_resume"
URL_RG_SEND = "http://localhost:5000/api/v1/send_registr"


def send_json(url, query):
    data = jsonify(query)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    response = requests.post(url=url, data=data, headers=headers, timeout=5)
    response.raise_for_status()
    return response


if __name__ == "__main__":
    res = [RESUME for _ in range(10)]
    print(jsonify(res))
