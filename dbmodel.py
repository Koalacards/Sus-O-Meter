from peewee import *

database = SqliteDatabase('suswords.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class ServerLanguage(BaseModel):
    id = IntegerField(null=True)
    language = TextField(null=True)

    class Meta:
        table_name = 'Server Language'
        primary_key = False

class SusWords(BaseModel):
    words = TextField(null=True)

    class Meta:
        table_name = 'Sus Words'
        primary_key = False

class SuswordsSpanish(BaseModel):
    words = TextField(null=True)

    class Meta:
        table_name = 'Sus words Spanish'
        primary_key = False

