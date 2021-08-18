from dbmodel import *

def get_sus_words_str():
    query = SusWords.select()
    for item in query:
        return item.words

def set_sus_words(words):
    query = SusWords.update(words=words)
    return query.execute()