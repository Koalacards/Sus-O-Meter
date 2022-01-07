from db.dbmodel import *

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

def set_server_list_type(id, list_type:str):
    query = CustomLists.select().where(CustomLists.id == id)
    if len(query) == 0:
        CustomLists.create(id=id, list_type=list_type, custom_list='[]')
    else:
        new_query = CustomLists.update(list_type=list_type).where(CustomLists.id == id)
        return new_query.execute()

def get_server_list_type(id):
    query = CustomLists.select().where(CustomLists.id == id)
    if len(query) == 0:
        return "Community"
    else:
        for item in query:
            return item.list_type

def set_server_custom_list(id, list_str:str):
    query = CustomLists.select().where(CustomLists.id == id)
    if len(query) == 0:
        CustomLists.create(id=id, list_type="Community", custom_list=list_str)
    else:
        new_query = CustomLists.update(custom_list=list_str).where(CustomLists.id == id)
        return new_query.execute()

def get_server_custom_list(id):
    query = CustomLists.select().where(CustomLists.id == id)
    if len(query) == 0:
        return []
    else:
        for item in query:
            return item.custom_list