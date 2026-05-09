from mongoengine import EmbeddedDocument, StringField, IntField

class Ubicacion(EmbeddedDocument):
    calle = StringField()
    numero = IntField()
    localidad = StringField()
    provincia = StringField()
