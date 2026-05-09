from mongoengine import Document, StringField

class Laboratorio(Document):
    nombre = StringField(required=True, unique=True)
    
    meta = {'collection': 'laboratorios'}
