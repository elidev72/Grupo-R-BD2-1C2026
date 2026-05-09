from mongoengine import Document, StringField, BooleanField, ListField, EmbeddedDocumentField, ReferenceField
from .ubicacion import Ubicacion
from .obra_social import ObraSocial
from .sucursal import Sucursal

class Persona(Document):
    dni = StringField(primary_key=True)
    nombre = StringField(required=True)
    apellido = StringField(required=True)
    domicilio = EmbeddedDocumentField(Ubicacion)
    obras_sociales = ListField(EmbeddedDocumentField(ObraSocial))
    
    
    es_empleado = BooleanField(default=False)
    # Este campo se llena si es empleado
    cuil = StringField(unique=True, sparse=True)
    sucursal_donde_trabaja = ReferenceField(Sucursal)
    es_encargado = BooleanField(default=False)
    
    
    meta = {
        'collection': 'personas',
        'indexes': ['apellido'] # para buscar clientes
    }
