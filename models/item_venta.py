from mongoengine import EmbeddedDocument, StringField, FloatField, IntField, ReferenceField
from .producto import Producto, Categoria

class ItemVenta(EmbeddedDocument):
    producto_id = ReferenceField(Producto, required=True)
    cantidad = IntField(default=1, min_value=1)
    precio_unitario = FloatField(required=True, min_value=0.01)
    categoria = StringField(choices=[c.value for c in Categoria], required=True)  # "Farmacia" o "Perfumeria" para Reporte 4

    @property
    def total_item(self) -> float:
        return self.precio_unitario * self.cantidad
