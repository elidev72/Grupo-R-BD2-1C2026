from enum import Enum
from mongoengine import Document, StringField, FloatField, ReferenceField
from .laboratorio import Laboratorio

class Categoria(Enum):
    FARMACIA = "farmacia"
    PERFUMERIA = "perfumería"

class Producto(Document):
    descripcion = StringField()
    precio = FloatField(required=True)
    categoria = StringField(choices=[c.value for c in Categoria], required=True) # "Farmacia" o "Perfumeria" del reporte 4
    laboratorio = ReferenceField(Laboratorio)
    
    meta = {'collection': 'productos'}
