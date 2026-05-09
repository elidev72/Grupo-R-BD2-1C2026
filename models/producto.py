from mongoengine import Document, StringField, FloatField, ReferenceField
from .laboratorio import Laboratorio

class Producto(Document):
    descripcion = StringField(required=True)
    precio = FloatField(required=True)
    categoria = StringField() # "Farmacia" o "Perfumeria" del reporte 4
    laboratorio = ReferenceField(Laboratorio)
    
    meta = {'collection': 'productos'}
