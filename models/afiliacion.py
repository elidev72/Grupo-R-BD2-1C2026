from mongoengine import EmbeddedDocument, ReferenceField, StringField, DateTimeField
from .obra_social import ObraSocial

class Afiliacion(EmbeddedDocument):
    obra_social = ReferenceField(ObraSocial, required=True)
    numero_afiliado = StringField(required=True)
    fecha_alta = DateTimeField(required=True)
