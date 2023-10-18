# pip install spacy
# pip install ru-core-news-sm
# pip install natasha

import re
import string
from collections import Counter

# import natasha
import spacy
from spacy.lang.ru.stop_words import STOP_WORDS

nlp = spacy.load("ru_core_news_sm")

def analyse_text(data: dict):

    list_data = [str(v) for _, v in data.items]
    
    lst = [item.lower() for item in list_data \
           if item.lower() not in STOP_WORDS and not item.isdigit()]

    text = ' '.join(list(lst)).strip()
    txt = text.replace('«', '').replace('»', '')
    txt = re.sub('\s+', ' ', txt)
    txt = txt.translate(str.maketrans('', '', string.punctuation))

    doc = nlp(txt)

    lemmas = [token.lemma_ for token in doc]
    word_frequency = Counter(lemmas)
    frequency = {word for word, freq in word_frequency.items() if freq > 1}

    named = {token for token in doc.ents}

    return frequency.union(named)

if __name__ == '__main__':
    dct = {}
    analyse_text(dct)