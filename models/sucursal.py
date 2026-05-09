from mongoengine import Document, StringField, EmbeddedDocumentField, ReferenceField
from .ubicacion import Ubicacion
from .cadena import Cadena

class Sucursal(Document):
    nombre = StringField(required=True)
    cadena = ReferenceField(Cadena, required=True)
    domicilio = EmbeddedDocumentField(Ubicacion)
    
    meta = {'collection': 'sucursales'}
