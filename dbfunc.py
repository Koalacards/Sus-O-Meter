from dbmodel import *

def get_sus_words_str():
    query = SusWords.select()
    for item in query:
        return item.words

def set_sus_words(words):
    query = SusWords.update(words=words)
    return query.execute()

def get_sus_words_spanish():
    query = SuswordsSpanish.select()
    for item in query:
        return item.words

def set_sus_words_spanish(words):
    query = SuswordsSpanish.update(words=words)
    return query.execute()

def set_server_language(id, language):
    query = ServerLanguage.select().where(ServerLanguage.id == id)
    if len(query) == 0:
        ServerLanguage.create(id=id, language=language)
    else:
        new_query = ServerLanguage.update(language=language).where(ServerLanguage.id == id)
        return new_query.execute()

def get_server_language(id):
    query = query = ServerLanguage.select().where(ServerLanguage.id == id)
    if len(query) == 0:
        return "English"
    else:
        for item in query:
            return item.language