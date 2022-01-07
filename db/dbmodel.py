from peewee import *

database = SqliteDatabase('db/suswords.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class BlacklistedWords(BaseModel):
    blacklisted = TextField(null=True)

    class Meta:
        table_name = 'Blacklisted Words'
        primary_key = False

class CustomLists(BaseModel):
    custom_list = TextField(null=True)
    id = IntegerField(null=True)
    list_type = TextField(null=True)

    class Meta:
        table_name = 'Custom Lists'
        primary_key = False

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

