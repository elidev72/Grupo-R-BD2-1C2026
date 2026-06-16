

#3. Un reporte con dos resultados, por un lado el total de la cobranza de toda la cadena
# completa (todas las sucursales) y por otro lado la cobranza agrupada por sucursales. Todo esto
# debe ocurrir entre dos fechas pasadas como parámetros (fecha desde y fecha hasta).

# intentar acceder a la coleccion usando el objeto como Venta (importar dependencia)
# Venta._get_collection().aggregate(codigo no sql)

# recomendacion hagan la consulta primero en el mongodb compass o lo que usen para
# abstraerse de problemas de codigo y una vez la tienen la intentan agregar al codigo

from datetime import datetime
from models.venta import Venta

def reporte_3(fecha_desde, fecha_hasta):
    collection = Venta._get_collection()

    pipeline = [
        {
            "$match": {
                "fecha": {
                    "$gte": fecha_desde,
                    "$lte": fecha_hasta
                }
            }
        },

       
        {
            "$facet": {
                
                "total_cadena": [
                    {
                        "$group": {
                            "_id": None,  
                            "totalCobranza": {
                                "$sum": {
                                    "$sum": {
                                        "$map": {
                                            "input": "$items",
                                            "as": "item",
                                            "in": { "$multiply": ["$$item.cantidad", "$$item.precio_unitario"] }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "descripcion": { "$literal": "Total Cadena Completa" },
                            "totalCobranza": { "$round": ["$totalCobranza", 2] }
                        }
                    }
                ],

                
                "por_sucursal": [
                    {
                        "$group": {
                            "_id": "$sucursal", 
                            "totalCobranza": {
                                "$sum": {
                                    "$sum": {
                                        "$map": {
                                            "input": "$items",
                                            "as": "item",
                                            "in": { "$multiply": ["$$item.cantidad", "$$item.precio_unitario"] }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    
                    {
                        "$lookup": {
                            "from": "sucursales",
                            "localField": "_id",
                            "foreignField": "_id",
                            "as": "sucursal_info"
                        }
                    },
                    {
                        "$unwind": {
                            "path": "$sucursal_info",
                            "preserveNullAndEmptyArrays": True 
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                           
                            "sucursal": { "$ifNull": ["$sucursal_info.nombre", "$_id"] }, 
                            "totalCobranza": { "$round": ["$totalCobranza", 2] }
                        }
                    },
                    {
                        "$sort": {
                            "totalCobranza": -1 
                        }
                    }
                ]
            }
        }
    ]

    resultado = list(collection.aggregate(pipeline))

    return resultado[0] if resultado else {"total_cadena": [], "por_sucursal": []}

def reporte_4(fecha_desde, fecha_hasta):
    collection = Venta._get_collection()

    pipeline = [
       
        {
            "$match": {
                "fecha": {
                    "$gte": fecha_desde,
                    "$lte": fecha_hasta
                }
            }
        },

        
        {
            "$unwind": "$items"
        },

        
        {
            "$group": {
                "_id": "$items.categoria",
                "cantidad_vendida": {
                    "$sum": "$items.cantidad"
                }
            }
        },

        
        {
            "$project": {
                "_id": 0,
                "tipo_producto": "$_id",
                "cantidad_vendida": 1
            }
        },
        
        
        {
            "$sort": {
                "tipo_producto": 1
            }
        }
    ]

    resultado = list(collection.aggregate(pipeline))
    
    return resultado  


def reporte_5():
    collection = Venta._get_collection()
    
    pipeline = [
        
        { "$unwind": "$items" },
        
        
        {
            "$group": {
                "_id": {
                    "sucursal": "$sucursal",
                    "producto_id": "$items.producto_id"
                },
                "monto_vendido": {
                    "$sum": { "$multiply": ["$items.cantidad", "$items.precio_unitario"] }
                }
            }
        },
        
    
        {
            "$lookup": {
                "from": "productos",
                "localField": "_id.producto_id",
                "foreignField": "_id",
                "as": "info_producto"
            }
        },
        {
            "$lookup": {
                "from": "sucursales",
                "localField": "_id.sucursal",
                "foreignField": "_id",
                "as": "info_sucursal"
            }
        },
        { "$unwind": "$info_producto" },
        { "$unwind": "$info_sucursal" },
        
    
        {
            "$project": {
                "_id": 0,
                "sucursal": "$info_sucursal.nombre",
                "producto": "$info_producto.descripcion",
                "monto_vendido": { "$round": ["$monto_vendido", 2] }
            }
        },
        
         
        {
            "$sort": { "monto_vendido": -1 }
        }
    ]
    
    return list(collection.aggregate(pipeline))