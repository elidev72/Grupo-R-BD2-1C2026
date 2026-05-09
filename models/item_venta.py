from mongoengine import EmbeddedDocument, StringField, FloatField, IntField, ReferenceField
from .producto import Producto

class ItemVenta(EmbeddedDocument):
    producto_id = ReferenceField(Producto)
    descripcion = StringField()
    cantidad = IntField(default=1)
    precio_unitario = FloatField(required=True)
    total_item = FloatField()
    categoria = StringField(required=True)  # "Farmacia" o "Perfumeria" para Reporte 4
