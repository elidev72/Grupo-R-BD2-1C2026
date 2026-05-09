from mongoengine import Document, DateTimeField, StringField, FloatField, ListField, EmbeddedDocumentField, ReferenceField
from .persona import Persona
from .sucursal import Sucursal
from .item_venta import ItemVenta
from .cadena import Cadena

class Venta(Document):
    fecha = DateTimeField(required=True)
    cadena = ReferenceField(Cadena)
    sucursal = ReferenceField(Sucursal)
    cliente = ReferenceField(Persona)
    empleado_atiende = ReferenceField(Persona)
    
    items = ListField(EmbeddedDocumentField(ItemVenta))
    
    total_a_pagar = FloatField()
    forma_pago = StringField(required=True)  # Reporte 3
    tipo_cliente = StringField(required=True) # "Obra Social" o "Privado" para Reporte 2

    meta = {
        'collection': 'ventas',
        'indexes': [
            ('cadena', 'fecha'),
            ('sucursal', 'fecha'),
            'tipo_cliente',
            'forma_pago'
        ]
    }
