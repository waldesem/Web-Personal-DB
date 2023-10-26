import re
import string

import spacy
from spacy.lang.ru.stop_words import STOP_WORDS


nlp = spacy.load("ru_core_news_sm")
# nlp = spacy.load("ru_core_news_md")


def clear_text(text):
    txt = text.replace('«', '').replace('»', '')
    txt = re.sub('\s+', ' ', txt)
    txt = txt.translate(str.maketrans('', '', string.punctuation))
    lst_txt = txt.split()
    lst = [item.lower() for item in lst_txt \
           if item.lower() not in STOP_WORDS and not item.isdigit()]
    txt = ' '.join(lst)
    return txt


def parse_text(text):

    lst_txt = text.split()

    list_data = [item.lower() for item in lst_txt if not item.isdigit()]

    digits = [digit for digit in lst_txt if digit.isdigit() and len(digit) > 3]

    dates = [d for d in list_data if re.match(r'\d\d.\d\d.\d\d\d\d', d) \
             or re.match(r'\d\d\d\d-\d\d-\d\d', d)]

    txt = ' '.join(list_data)

    doc = nlp(txt)

    lemmas = [token.lemma_ for token in doc if token.pos_]
    
    names = [token.text for token in doc.ents]


    return  {'digits': digits, 'dates': dates, 'lemmas': lemmas, 'names': names }


def get_similarity(data, template):
    
    origin = nlp(data)
    temp = nlp(template)
    similar = temp.similarity(origin)
    print(similar)

    return similar


if __name__ == "__main__":
    query = 'Найти кандидата Петров Алексей'
    template = 'Облачно без осадков'

    get_similarity(query, template)

    get_similarity(
        clear_text(query),
        clear_text(template)
    )
