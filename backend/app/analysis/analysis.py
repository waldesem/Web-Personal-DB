import re
import string
from datetime import datetime as dt

import spacy
from spacy.lang.ru.stop_words import STOP_WORDS


from .. import db
from ..models.model import  Person, Document

templates = {
    'anketa': 'Поиск: фамилия имя дата рождения паспорт серия номер инн снилс',
    'check': 'Поиск: результат проверка кандидата'
}
    
class Analysis:

    def __init__(self, text) -> None:
        self.nlp = spacy.load("ru_core_news_md")
        self.text = text.lower()
        self.doc = self.nlp(self.text)
        self.names = []
        self.digits = []
        self.dates = []

    def clear_text(self):
        txt = self.text.replace('«', '').replace('»', '')
        txt = re.sub('\s+', ' ', txt)
        txt = txt.translate(str.maketrans('', '', string.punctuation))
        return txt

    def get_names(self):
        return [ent.text for ent in self.doc.ents if ent.label_ == 'PER']

    def get_company(self):
        return [token.text for token in self.doc.ents if token.label_ == 'ORG'][0]

    def get_digits(self):
        lst_txt = self.text.split()
        return [digit for digit in lst_txt if digit.isdigit()]


    def get_date(self):
        lst_txt = self.text.split()
        return [d for d in lst_txt if re.match(r'\d\d\.\d\d\.\d\d\d\d', d) \
                or re.match(r'\d\d\d\d-\d\d-\d\d', d)]


    def get_lemmas(self):
        lst_txt = self.text.split()
        list_data = [item.lower() for item in lst_txt \
                    if not item.isdigit() and item.lower() not in STOP_WORDS]
        doc = self.nlp(' '.join(list_data))
        return  [token.lemma_ for token in doc if token.pos_]


    def get_similarity(self, template):
        template_nlp = self.nlp(template)
        return template_nlp.similarity(self.doc)

    def get_values(self):
        self.names = self.get_names()
        self.digits = self.get_digits()
        self.dates = self.get_date()
        return {
            'names': self.names,
            'digits': self.digits,
            'dates': self.dates
        }
            

class Actions(Analysis):
    
    def __init__(self,  response):
        self.response = response
        self.names_string = ''
        self.series_passport = ''
        self.number_passport = ''
        self.inn = ''
        self.snils = ''
        self.data_string = ''

    def names_actions(self):
        if self.response['names']:
            self.names_string = ' '.join(self.response['names'])
        return self.names_string 
    
    def digits_actions(self):
        if len(self.response['digits']):
            for digit in self.response['digits']:
                match len(digit):
                    case 4:
                        self.series_passport = str(digit)
                    case 6:
                        self.number_passport = str(digit)
                    case 12:
                        self.inn = str(digit)
                    case 11:
                        self.snils = str(digit)
        return {
            'series_passport': self.series_passport,
            'number_passport': self.number_passport,
            'inn': self.inn,
            'snils': self.snils
            }
                    
    def dates_actions(self):
        if self.response['dates']:
            if re.match(r'\d\d\.\d\d\.\d\d\d\d', self. response['dates'][0]):
                self.data_string = dt.strptime(self.response['dates'][0], '%d.%m.%Y')
            else:
                self.data_string = dt.strptime(self.response['dates'][0], '%Y-%m-%d')
        return self.data_string 


def parse_data(json_data):
    analysis = Analysis(json_data['data'])
    similars = {str(analysis.get_similarity(v)): k for k, v in templates.items()}
    max_sim = max([float(sim) for sim in similars])
    if max_sim > 0.5:
        template = similars[str(max_sim)]
        match template:
            case 'anketa':
                results = analysis.get_values()
                if results:
                    rules = Actions(results)
                    name = rules.names_actions()
                    digits = rules.digits_actions()
                    data = rules.dates_actions()

                    query = db.session.query(Person).order_by(Person.id.desc())
                    query = query.filter(
                        Person.fullname.ilike('%{}%'.format(name)),
                        Person.birthday == data.strftime('%Y-%m-%d') if data else True,
                        Person.inn.ilike('%{}%'.format(digits['inn'])),
                        Person.snils.ilike('%{}%'.format(digits['snils']))
                        ).join(Document, isouter=True).filter(
                            Document.series.ilike('%{}%'.format(digits['series_passport'])),
                            Document.number.ilike('%{}%'.format(digits['number_passport']))
                        ).limit(10).all()
                    if query:
                        result = [f'id {item.id} - {item.fullname}' for item in query]
                        return ['anketa', result, len(query)]
    return ['error', {}]