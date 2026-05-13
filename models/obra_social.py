from enum import Enum
from mongoengine import Document, StringField

class NombreEmpresa(Enum):
    IOMA = 'IOMA'
    OSDE = 'OSDE'
    SM = 'Swiss Medica'
    PAMI = 'PAMI'
    OSECAC = 'OSECAC'

class ObraSocial(Document):
    nombre = StringField(choices=[n.value for n in NombreEmpresa], required=True)
