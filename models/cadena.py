from mongoengine import Document, StringField

class Cadena(Document):
    nombre = StringField(required=True, unique=True) # Marca comercial
    cuit = StringField()

    meta = {'collection': 'cadenas'}
