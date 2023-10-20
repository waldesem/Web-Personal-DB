import re
import string
from collections import Counter

# import natasha
import spacy
from spacy.lang.ru.stop_words import STOP_WORDS

import random
from faker import Faker

fake = Faker("ru-RU")

nlp = spacy.load("ru_core_news_sm")

def analyse_text(data: dict):

    list_data = [str(v) for k, v in data.items() if k not in ['id', 'request_id', 'person_id']]
    
    digital = {digit for digit in list_data if digit.isdigit()}

    dates = {d for d in list_data if re.match(r'\d\d.\d\d.\d\d\d\d', d) or re.match(r'\d\d\d\d-\d\d-\d\d', d)}

    lst = [item.lower() for item in list_data \
           if item.lower() not in STOP_WORDS]

    text = ' '.join(list(lst)).strip()
    txt = text.replace('«', '').replace('»', '')
    txt = re.sub('\s+', ' ', txt)
    txt = txt.translate(str.maketrans('', '', string.punctuation))
    
    doc = nlp(txt)

    lemmas = [token.lemma_ for token in doc \
              if token.pos_ == 'NOUN' or token.pos_ == 'VERB']
    word_frequency = Counter(lemmas)
    frequency = {word for word, freq in word_frequency.items() if freq > 1}

    named = {token for token in doc.ents}

    return frequency.union(named).union(digital).union(dates)

if __name__ == '__main__':
    resume = {
        "id": 1,
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
    }
    check = {
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
    for s in [resume, check]:
        tag_set = analyse_text(s)
        print(tag_set)