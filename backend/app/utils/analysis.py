import re
import string

import spacy
from spacy.lang.ru.stop_words import STOP_WORDS


class Analysis:

    def __init__(self, text) -> None:
        self.nlp = spacy.load("ru_core_news_sm")
        # nlp = spacy.load("ru_core_news_md")
        self.text = text
        self.doc = self.nlp(self.text)

    def clear_text(self):
        txt = self.text.replace('«', '').replace('»', '')
        txt = re.sub('\s+', ' ', txt)
        txt = txt.translate(str.maketrans('', '', string.punctuation))
        return txt

    def get_names(self):
        return [token.text for token in self.doc.ents]


    def get_digits(self):
        lst_txt = self.text.split()
        return [digit for digit in lst_txt if digit.isdigit()]


    def get_dates(self):
        lst_txt = self.text.split()
        return [d for d in lst_txt if re.match(r'\d\d.\d\d.\d\d\d\d', d) \
                or re.match(r'\d\d\d\d-\d\d-\d\d', d)]


    def get_lemmas(self):
        lst_txt = self.text.split()
        list_data = [item.lower() for item in lst_txt \
                    if not item.isdigit() and item.lower() not in STOP_WORDS]
        doc = self.nlp(' '.join(list_data))
        return  [token.lemma_ for token in doc if token.pos_]


    def get_similarity(self, template):
        template_nlp = self.nlp(template)
        similar =  template_nlp.similarity(self.nlp)
        names = []
        if similar > 0.1:
            names = self.get_names(self.text)
        return names

if __name__ == "__main__":
    query = 'Поиск кандидата Петров Алексей'
    template = 'Найти кандидата'

    analysis = Analysis(query)
    print(analysis.get_similarity(template))