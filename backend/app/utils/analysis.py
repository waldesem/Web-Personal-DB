# pip install spacy
# pip install ru-core-news-sm

import string
from collections import Counter

import spacy
from spacy.lang.ru.stop_words import STOP_WORDS

nlp = spacy.load("ru_core_news_sm")

def analyse_text(data: dict):

    data = {k: str(v) for k, v in data.items}

    lst_origin = list(data.values())
    
    lst = [item.lower() for item in lst_origin if not item.isdigit() and not item.isalpha()]
    lst = [item for item in lst if item not in STOP_WORDS]
    text = ' '.join(list(lst))
    txt = text.replace('«', '').replace('»', '').replace('—', '').replace('-', '')
    txt = txt.translate(str.maketrans('', '', string.punctuation))

    doc = nlp(txt)
    lemmas = [token.lemma_ for token in doc if token.pos_ == 'NOUN' or token.pos_ == 'VERB']
    word_frequency = Counter(lemmas)
    frequency = {word for word, freq in word_frequency.items() if freq > 1}
    
    text_2 = ' '.join(list(lst_origin))
    doc1 = nlp(text_2)
    named = {ent.text for ent in doc1.ents}

    return frequency.update(named)
