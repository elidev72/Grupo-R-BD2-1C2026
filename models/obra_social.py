from mongoengine import EmbeddedDocument, StringField

class ObraSocial(EmbeddedDocument):
    nombre = StringField(required=True)
    nro_afiliado = StringField()
