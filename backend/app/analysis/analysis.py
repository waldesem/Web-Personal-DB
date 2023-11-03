import re
import string
from datetime import datetime as dt

import spacy
from spacy.lang.ru.stop_words import STOP_WORDS

from ..models.model import  Person

nlp = spacy.load("ru_core_news_md")


class Analysis:

    def __init__(self, text) -> None:
        self.text = text.lower()
        self.doc = nlp(self.text)
        self.names = ''
        self.digits = ''
        self.dates = ''
        self.lemmas = ''

    def clear_text(self):
        txt = self.text.replace('«', '').replace('»', '')
        txt = re.sub('\s+', ' ', txt)
        txt = txt.translate(str.maketrans('', '', string.punctuation))
        return txt

    def get_names(self):
        entities = [ent.text for ent in self.doc.ents]
        if len(entities):
            self.names = ' '.join(entities)

    def get_digits(self):
        lst_txt = self.text.split()
        digits = [digit for digit in lst_txt if digit.isdigit()]
        if len(digits):
            for digit in digits:
                match len(digit):
                    case 4:
                        self.series_passport = str(digit)
                    case 6:
                        self.number_passport = str(digit)
                    case 12:
                        self.inn = str(digit)
                    case 11:
                        self.snils = str(digit)
            self.digits = f"{self.series_passport} {self.number_passport} {self.inn} {self.snils}"

    def get_date(self):
        lst_txt = self.text.split()
        datas =  [d for d in lst_txt if re.match(r'\d\d\.\d\d\.\d\d\d\d', d) \
                or re.match(r'\d\d\d\d-\d\d-\d\d', d)]
        if len(datas):
            dates = []
            for data in datas:
                if re.match(r'\d\d\.\d\d\.\d\d\d\d', data):
                    dates.append(dt.strptime(data, '%d.%m.%Y'))
                else:
                    dates.append(dt.strptime(data, '%Y-%m-%d'))
            self.dates = ' '.join([str(item) for item in dates])

    def get_lemmas(self):
        txt = self.clear_text()
        lst_txt = txt.split()
        list_data = [item.lower() for item in lst_txt \
                    if not item.isdigit() and item.lower() not in STOP_WORDS]
        doc = nlp(' '.join(list_data))
        lemmas =  [token.lemma_ for token in doc if token.pos_]
        if len(lemmas):
            self.lemmas = ' '.join(lemmas)

    def get_similarity(self, template):
        template_nlp = nlp(template)
        return template_nlp.similarity(self.doc)

    def parse_data(self):
        summary = f"{self.names} {self.digits} {self.dates} {self.lemmas}"
        if summary:
            query = Person.opensearch(f"{self.names} {self.digits} \
                                  {self.dates} {self.lemmas}")
            if query:
                return '; '.join([f'id {item.id} - {item.fullname}' for item in query])                       
        return ''
