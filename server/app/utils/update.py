import urllib
import sqlite3
import os
import csv
import bz2
import codecs

import requests
from bs4 import BeautifulSoup as bs
from flask_apscheduler import APScheduler

basedir = os.path.abspath(os.path.dirname(__file__))


scheduler = APScheduler()
DB = os.path.join(basedir, 'resourses.db')


def sqlite_upd(query):
    try:
        with sqlite3.connect(DB) as con:
            cur = con.cursor()
            cur.execute(query)
            con.commit()
    except sqlite3.Error as error:
        print(error)
            

# @scheduler.task('cron', id='disqual', day_of_week='fri', hour='21', minute='00')
# def disqual():
#     page = requests.get('https://www.nalog.gov.ru/opendata/7707329152-registerdisqualified/')
#     soup = bs(page.text, "html.parser")
#     items = soup.find('table', class_='border_table')
#     href = items.find('a', href=True)
    
#     if 'registerdisqualified' in str(href):
#         url_disqual = ''.join(href['href'])
#         file = urllib.request.urlopen(url_disqual)
#         reader = csv.reader(codecs.iterdecode(file, 'utf-8'))
#         if reader:
#             columns = next(reader)
#             column = ', '.join(''.join(columns).split(';'))
#             sqlite_upd("DROP TABLE IF EXISTS disqual")
#             sqlite_upd(f"CREATE TABLE disqual ({column})")
#             query = 'INSERT INTO disqual({0}) values ({1})'
#             query = query.format(column, ', '.join('?' * len(''.join(columns).split(';'))))
            
#             with sqlite3.connect(DB) as con:
#                 cursor = con.cursor()
#                 for data in reader:
#                     cursor.execute(query, ''.join(data).split(';'))
#                 con.commit()
        
        
# @scheduler.task('cron', id='passport', day_of_week='mon-fri', hour='21')
def passport():
    with open('/home/semenenko/Загрузки/list_of_expired_passports.csv') as file:
        reader = csv.reader(file)
        if reader:
            columns = next(reader)
            column = ', '.join(''.join(columns).split(';'))
            sqlite_upd("DROP TABLE IF EXISTS passport")
            sqlite_upd(f"CREATE TABLE passport ({column})")
            query = 'INSERT INTO passport({0}) values ({1})'
            query = query.format(column, ', '.join('?' * len(''.join(columns).split(';'))))
        
            with sqlite3.connect(DB) as con:
                cursor = con.cursor()
                for data in reader:
                    cursor.execute(query, ''.join(data).split(';'))
                con.commit()
            sqlite_upd('CREATE UNIQUE INDEX idx_passport ON passport (PASSP_NUMBER)')

passport()