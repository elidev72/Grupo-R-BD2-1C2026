from mongoengine import Document, StringField, BooleanField, EmbeddedDocumentField, ReferenceField
from .ubicacion import Ubicacion
from .afiliacion import Afiliacion
from .sucursal import Sucursal

class Persona(Document):
    dni = StringField(primary_key=True)
    nombre = StringField(required=True)
    apellido = StringField(required=True)
    domicilio = EmbeddedDocumentField(Ubicacion, required=True)
    afiliacion = EmbeddedDocumentField(Afiliacion)
    
    es_empleado = BooleanField(default=False)
    # Este campo se llena si es empleado
    cuil = StringField(unique=True, sparse=True) # sparse=True permite que existan múltiples empleados sin este campo
    sucursal_donde_trabaja = ReferenceField(Sucursal)
    es_encargado = BooleanField(default=False)
    
    meta = {
        'collection': 'personas',
        'indexes': ['apellido'] # para buscar clientes
    }
