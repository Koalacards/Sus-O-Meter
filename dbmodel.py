from peewee import *

database = SqliteDatabase('suswords.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class SusWords(BaseModel):
    words = TextField(null=True)

    class Meta:
        table_name = 'Sus Words'
        primary_key = False

