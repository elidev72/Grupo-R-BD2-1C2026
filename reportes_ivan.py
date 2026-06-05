from models.venta import Venta

def reporte_1(fecha_desde, fecha_hasta):
    collection = Venta._get_collection()

    pipeline_total = [
        {
            "$match": {
                "fecha": {
                    "$gte": fecha_desde,
                    "$lte": fecha_hasta
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "totalVentas": {"$sum": 1}
            }
        }
    ]

    pipeline_por_sucursal = [
        {
            "$match": {
                "fecha": {
                    "$gte": fecha_desde,
                    "$lte": fecha_hasta
                }
            }
        },
        {
            "$group": {
                "_id": "$sucursal",
                "totalVentas": {"$sum": 1}
            }
        }
    ]

    return {
        "total_general": list(collection.aggregate(pipeline_total)),
        "por_sucursal": list(collection.aggregate(pipeline_por_sucursal))
    }

#1. Un reporte con dos resultados, por un lado el total de la cantidad de ventas de toda la
#cadena completa (todas las sucursales) y por otro lado las cantidades de ventas agrupadas por
#sucursales. Todo esto debe ocurrir entre dos fechas pasadas como parámetros (fecha desde y
#fecha hasta)

# intentar acceder a la coleccion usando el objeto como Venta (importar dependencia)
# Venta._get_collection().aggregate(codigo no sql)

# recomendacion hagan la consulta primero en el mongodb compass o lo que usen para
# abstraerse de problemas de codigo y una vez la tienen la intentan agregar al codigo





#
#2. Un reporte con las cantidades de ventas agrupadas por obras sociales y además considerar
#los privados (sin obra social) como un grupo mas. Todo esto debe ocurrir entre dos fechas
#pasadas como parámetros (fecha desde y fecha hasta)



def reporte_2(fecha_desde, fecha_hasta):
    collection = Venta._get_collection()

    pipeline = [
        # 1. filtro por fechas
        {
            "$match": {
                "fecha": {
                    "$gte": fecha_desde,
                    "$lte": fecha_hasta
                }
            }
        },

        # 2. join con personas
        {
            "$lookup": {
                "from": "personas",
                "localField": "cliente",
                "foreignField": "_id",
                "as": "cliente_info"
            }
        },

        # 3. unwind cliente
        {
            "$unwind": "$cliente_info"
        },

        # 4. join obra social
        {
            "$lookup": {
                "from": "obra_social",  # ojo: puede variar el nombre
                "localField": "cliente_info.afiliacion.obra_social",
                "foreignField": "_id",
                "as": "obra_social_info"
            }
        },

        # 5. unwind obra social (para poder agrupar bien)
        {
            "$unwind": {
                "path": "$obra_social_info",
                "preserveNullAndEmptyArrays": True
            }
        },

        # 6. group final
        {
            "$group": {
                "_id": {
                    "$ifNull": [
                        "$obra_social_info.nombre",
                        "Privado"
                    ]
                },
                "cantidadVentas": {
                    "$sum": 1
                }
            }
        }
    ]

    return list(collection.aggregate(pipeline))



#
#6. Ranking de cantidad de productos vendidos, agrupado por producto y por sucursal.

from models.venta import Venta

def reporte_6():
    collection = Venta._get_collection()

    pipeline = [
        {
            "$unwind": "$items"
        },
        {
            "$group": {
                "_id": {
                    "producto": "$items.producto_id",
                    "sucursal": "$sucursal"
                },
                "totalVendidos": {
                    "$sum": "$items.cantidad"
                }
            }
        },
        {
            "$sort": {
                "totalVendidos": -1
            }
        }
    ]

    return list(collection.aggregate(pipeline))

