from enum import Enum
from mongoengine import Document, DateTimeField, StringField, FloatField, ListField, EmbeddedDocumentField, ReferenceField
from .persona import Persona
from .sucursal import Sucursal
from .item_venta import ItemVenta
from .cadena import Cadena

class FormaPago(Enum):
    E = 'Efectivo'
    T = 'Transferencia bancaria'
    D = 'Tarjeta de débito'
    C = 'Tarjeta de crédito'

class TipoCliente(Enum):
    O = 'obra social'
    P = 'privado'

class Venta(Document):
    fecha = DateTimeField(required=True)
    cadena = ReferenceField(Cadena, required=True)
    sucursal = ReferenceField(Sucursal, required=True)
    cliente = ReferenceField(Persona, required=True)
    empleado_atiende = ReferenceField(Persona, required=True)
    
    items = ListField(EmbeddedDocumentField(ItemVenta, required=True))
    
    forma_pago = StringField(choices=[f.value for f in FormaPago], required=True)  # Reporte 3
    tipo_cliente = StringField(choices=[t.value for t in TipoCliente], required=True) # "Obra Social" o "Privado" para Reporte 2

    @property
    def total_a_pagar(self) -> float:
        return sum(item.total_item for item in self.items)

    meta = {
        'collection': 'ventas',
        'indexes': [
            ('cadena', 'fecha'),
            ('sucursal', 'fecha'),
            'tipo_cliente',
            'forma_pago'
        ]
    }
