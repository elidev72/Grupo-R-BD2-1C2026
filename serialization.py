import json
from datetime import datetime
from bson import ObjectId

from models import *
from config import conectar_db, desconectar_db

class MongoEncoder(json.JSONEncoder):
    """
    Encoder personalizado para transformar ObjectIds y objetos datetime 
    en formatos que el JSON estándar pueda escribir sin tirar error.
    """
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def serializar_documento_venta(v: Venta) -> dict:
    info_cliente = {
        "dni": v.cliente.dni,
        "nombre": v.cliente.nombre,
        "apellido": v.cliente.apellido,
        "tipo_cliente": v.tipo_cliente
    }
    
    if v.cliente.afiliacion and v.tipo_cliente == 'obra social':
        info_cliente["obra_social"] = {
            "nombre": v.cliente.afiliacion.obra_social.nombre,
            "numero_afiliado": v.cliente.afiliacion.numero_afiliado
        }

    info_empleado = {
        "id_empleado": v.empleado_atiende.id,
        "nombre": v.empleado_atiende.nombre,
        "apellido": v.empleado_atiende.apellido,
        "cuil": v.empleado_atiende.cuil
    }
    
    info_sucursal = {
        "id_sucursal": v.sucursal.id,
        "nombre": v.sucursal.nombre,
        "ubicacion": {
            "calle": v.sucursal.sede.calle,
            "numero": v.sucursal.sede.numero,
            "localidad": v.sucursal.sede.localidad,
            "provincia": v.sucursal.sede.provincia
        }
    }

    info_cadena = {
        "id_cadena": v.cadena.id,
        "nombre": v.cadena.nombre,
        "cuit": v.cadena.cuit
    }
    
    lista_items = []
    for item in v.items:
        prod = item.producto_id 
        
        lista_items.append({
            "id_producto": prod.id,
            "descripcion": prod.descripcion,
            "laboratorio": prod.laboratorio.nombre if prod.laboratorio else "Sin Laboratorio",
            "cantidad": item.cantidad,
            "precio_unitario": item.precio_unitario,
            "categoria": item.categoria,     
            "subtotal": item.total_item      
        })
        
    return {
        "id_venta": v.id,
        "fecha": v.fecha,
        "forma_pago": v.forma_pago,
        "cadena": info_cadena,
        "sucursal": info_sucursal,
        "cliente": info_cliente,
        "empleado_atiende": info_empleado,
        "items": lista_items,
        "total_venta": v.total_a_pagar
    }

if __name__ == '__main__':
    conectar_db()

    ventas = Venta.objects.all().select_related(max_depth=2)
    total_ventas = total_ventas = len(ventas)

    if total_ventas != 0:
        print(f"Procesando y desnormalizando {total_ventas} ventas...")
        
        datos_serializados = [serializar_documento_venta(v) for v in ventas]
        
        archivo_salida = 'entrega_final.json'
        print(f"Guardando estructura completa en '{archivo_salida}'...")
        
        with open(archivo_salida, 'w', encoding='utf-8') as f:
            json.dump(datos_serializados, f, cls=MongoEncoder, indent=4, ensure_ascii=False)
            
        print(f"Archivo '{archivo_salida}' listo.")

    desconectar_db()