from datetime import date
import sqlite3
import os
import datetime
import shutil
import requests

import dramatiq
from flask_melodramatiq import RabbitmqBroker
import aiohttp
import asyncio

from app.utils.update import DB
from ..utils.excel import BASE_PATH
from ..models.model import db, Candidate, Status

broker = RabbitmqBroker()
dramatiq.set_broker(broker)


@dramatiq.actor
def task_queue(anketa):
    check = Check(anketa)
    result = check.main()
    if result:
        check_result(result)
        return 'OK'
    else:
        return 'None'


def check_result(response):
    """
    Receives a payload containing information about a candidate check,
    including the candidate ID and status. If the status is REPLY, it copies
    files from a source directory to a destination directory, sets the
    candidate's status to REPLY, and creates a new check record. If the status
    is not REPLY, it sets the candidate's status to ERROR.
    :param response: A dictionary containing the following keys: id (int),
        autostatus (str), path (str), and any other keys required by the
        CheckSchema.
    """
    print(response)
    # result = db.session.get(Candidate, response['id'])
    # if response['autostatus'] == Status.REPLY.value:
    #     # Set the candidate's status to REPLY.
    #     result.status = Status.REPLY.value
    #     # Create a path for the candidate's files.
    #     path = os.path.join(
    #         BASE_PATH, result.fullname[0], f"{str(result.id)}-{result.fullname}",
    #         datetime.now().strftime("%Y-%m-%d"))
    #     # Copy files from the source directory to the destination directory.
    #     if response['path']:
    #         try:
    #             for file in os.listdir(response['path']):
    #                 shutil.copyfile(file, path)
    #         except FileNotFoundError as e:
    #             response['autostatus'] = f'{e}'
    #     # Update the response dictionary with the candidate ID and path.
    #     response["cand_id"] = response.pop('id')
    #     response["path"] = path
    #     # Create a new check record.
    #     check_dict = response | {"deadline": datetime.now()}
    #     db.session.add(Check(**check_dict))
    # else:
    #     # Set the candidate's status to ERROR.
    #     result.status = Status.ERROR.value
    # db.session.commit()


class Check:

    def __init__(self, anketa: dict) -> None:
        self.anketa = anketa
    
    def main(self):
        inn = self.check_inn(self.anketa)
        taxpayer = self.taxpayer_status(self.anketa)
        disqual = self.sqlite_resp("SELECT G2, G3 FROM dusqual WHERE G2={} and G3={}"
                                   .format(self.anketa['fullname'], self.anketa['birthday']))
        passport = self.sqlite_resp("SELECT PASSP_SERIES, PASSP_NUMBER FROM passport WHERE PASSP_SERIES={} and PASSP_NUMBER={}"
                                    .format(self.anketa['document']['series'], self.anketa['document']['number']))
        return {'cand_id': self.anketa['id'], 
                'passport': passport,
                'taxpayer': taxpayer,
                'disqual': disqual,
                'inn': inn, 
                'autostatus': Status.REPLY.value,
                'path': None}
        
    @classmethod
    def sqlite_resp(self, query):
        try:
            with sqlite3.connect(DB) as con:
                cur = con.cursor()
                cur.execute(query)
                record = cur.fetchall()
                return record
        except sqlite3.Error as error:
            return error
        
    # проверка инн
    def check_inn(self, anketa):
        url_inn = "https://service.nalog.ru/inn-proc.do"
        data_inn = {
            "fam": anketa["fullname"].split()[0],
            "nam": anketa["fullname"].split()[1],
            "otch": anketa["fullname"].split()[2],
            "bdate": anketa["birthday"],
            "bplace": "",
            "doctype": '21',
            "docno": f'{anketa["passport"]["series"][:2]} \
                {anketa["passport"]["series"][2:4]} \
                    {anketa["passport"]["number"]}',
            "docdt": anketa.issue,
            "c": "innMy",
            "captcha": "",
            "captchaToken": "",
            }
        try:
            inn_resp = requests.post(url=url_inn, data=data_inn)
            inn_resp.raise_for_status()
            response = inn_resp.json()
        except ConnectionError as error:
            response = error
        return response

    # проверка самозанятого
    def taxpayer_status(self, anketa):
        url_npd = "https://statusnpd.nalog.ru/api/v1/tracker/taxpayer_status"
        data_npd = {
        "inn": anketa["inn"], 
        "requestDate": date.today().isoformat(),
        }
        try:
            npd_resp = requests.post(url=url_npd, json=data_npd)
            npd_resp.raise_for_status()
            response = npd_resp.json()
        except ConnectionError as error:
            response = error
        return response
