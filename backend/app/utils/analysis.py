import re
import string

import spacy
from spacy.lang.ru.stop_words import STOP_WORDS

from .. import db
from ..models.model import Tag

nlp = spacy.load("ru_core_news_sm")

def analyse_text(data: dict):

    list_data = [str(v) for v in data.values()]
    
    digital = {digit for digit in list_data if digit.isdigit() and len(digit) > 3}

    dates = {d for d in list_data if re.match(r'\d\d.\d\d.\d\d\d\d', d) \
             or re.match(r'\d\d\d\d-\d\d-\d\d', d)}

    lst = [item.lower() for item in list_data \
           if item.lower() not in STOP_WORDS and not item.isdigit()]

    text = ' '.join(list(lst)).strip()
    txt = text.replace('«', '').replace('»', '')
    txt = re.sub('\s+', ' ', txt)
    txt = txt.translate(str.maketrans('', '', string.punctuation))
    
    doc = nlp(txt)

    lemmas = {token.lemma_ for token in doc if token.pos_ in ('PROPN', 'NOUN', 'VERB')}
    
    named = {token.text for token in doc.ents}

    return  lemmas.union(named).union(digital).union(dates)


def update_tags(new_tags: set, person_id: string):
    tags = db.session.query(Tag).filter_by(person_id=person_id).first()
    
    if tags:
        result = new_tags.union(set(tags.tag.split(' ')))
        tags.tag = ' '.join(result)
    else:
        db.session.add(Tag(tag=' '.join(new_tags), person_id=person_id))
    
    db.session.commit()