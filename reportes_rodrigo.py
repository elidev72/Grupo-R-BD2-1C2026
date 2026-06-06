

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

    pipeline = [
        {
            "$match": {
                "fecha": {
                    "$gte": fecha_desde,
                    "$lte": fecha_hasta
                }
            }
        },

        # Calcular total de cada venta
        {
            "$project": {
                "fecha": 1,
                "sucursal": 1,
                "forma_pago": 1,
                "total_venta": {
                    "$sum": {
                        "$map": {
                            "input": "$items",
                            "as": "item",
                            "in": {
                                "$multiply": [
                                    "$$item.cantidad",
                                    "$$item.precio_unitario"
                                ]
                            }
                        }
                    }
                }
            }
        },

        {
            "$facet": {

                # Detalle de ventas
                "detalle": [
                    {
                        "$lookup": {
                            "from": "sucursales",
                            "localField": "sucursal",
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
                            "fecha": 1,
                            "forma_pago": 1,
                            "total_venta": 1,
                            "sucursal": "$sucursal_info.nombre"
                        }
                    }
                ],

                # Total cadena por medio de pago
                "total_cadena_por_medio": [
                    {
                        "$group": {
                            "_id": "$forma_pago",
                            "total_cobrado": {
                                "$sum": "$total_venta"
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "medio_pago": "$_id",
                            "total_cobrado": 1
                        }
                    }
                ],

                # Total por sucursal y medio de pago
                "total_sucursal_por_medio": [
                    {
                        "$group": {
                            "_id": {
                                "sucursal": "$sucursal",
                                "medio_pago": "$forma_pago"
                            },
                            "total_cobrado": {
                                "$sum": "$total_venta"
                            }
                        }
                    },

                    {
                        "$lookup": {
                            "from": "sucursales",
                            "localField": "_id.sucursal",
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
                            "sucursal": "$sucursal_info.nombre",
                            "medio_pago": "$_id.medio_pago",
                            "total_cobrado": 1
                        }
                    },

                    {
                        "$sort": {
                            "sucursal": 1,
                            "medio_pago": 1
                        }
                    }
                ]
            }
        }
    ]

    resultado = list(Venta._get_collection().aggregate(pipeline))

    return resultado[0] if resultado else {
        "detalle": [],
        "total_cadena_por_medio": [],
        "total_sucursal_por_medio": []
    }

def mostrar_reporte_3(resultado):
    print("\n" + "="*60)
    print("DETALLE DE COBRANZA")
    print("="*60)

    for venta in resultado["detalle"]:
        print(
            f"Fecha: {venta['fecha']} | "
            f"Sucursal: {venta['sucursal']} | "
            f"Pago: {venta['forma_pago']} | "
            f"Total: ${venta['total_venta']:.2f}"
        )

    print("\n" + "="*60)
    print("TOTAL CADENA POR MEDIO DE PAGO")
    print("="*60)

    for item in resultado["total_cadena_por_medio"]:
        print(
            f"{item['medio_pago']}: "
            f"${item['total_cobrado']:.2f}"
        )

    print("\n" + "="*60)
    print("TOTAL POR SUCURSAL Y MEDIO DE PAGO")
    print("="*60)

    for item in resultado["total_sucursal_por_medio"]:
        print(
            f"Sucursal: {item['sucursal']} | "
            f"Pago: {item['medio_pago']} | "
            f"Total: ${item['total_cobrado']:.2f}"
        )

#4. Un reporte con las cantidades de ventas agrupadas por tipo de producto (farmacia /
#perfumería). Todo esto debe ocurrir entre dos fechas pasadas como parámetros (fecha desde y
#fecha hasta)

def reporte_4(fecha_desde, fecha_hasta):

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
            "$facet": {
                "total_cadena": [
                    {
                        "$group": {
                            "_id": "$items.categoria",
                            "cantidad_total": {
                                "$sum": "$items.cantidad"
                            },
                            "importe_total": {
                                "$sum": {
                                    "$multiply": [
                                        "$items.cantidad",
                                        "$items.precio_unitario"
                                    ]
                                }
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": 0,
                            "categoria": "$_id",
                            "cantidad_total": 1,
                            "importe_total": 1
                        }
                    }
                ],
                "total_por_sucursal": [
                    {
                        "$group": {
                            "_id": {
                                "sucursal": "$sucursal",
                                "categoria": "$items.categoria"
                            },
                            "cantidad_total": {
                                "$sum": "$items.cantidad"
                            },
                            "importe_total": {
                                "$sum": {
                                    "$multiply": [
                                        "$items.cantidad",
                                        "$items.precio_unitario"
                                    ]
                                }
                            }
                        }
                    },

                    {
                        "$lookup": {
                            "from": "sucursales",
                            "localField": "_id.sucursal",
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
                            "sucursal": "$sucursal_info.nombre",
                            "categoria": "$_id.categoria",
                            "cantidad_total": 1,
                            "importe_total": 1
                        }
                    },

                    {
                        "$sort": {
                            "sucursal": 1,
                            "categoria": 1
                        }
                    }
                ]
            }
        }
    ]

    resultado = list(Venta._get_collection().aggregate(pipeline))

    return resultado[0] if resultado else {
        "total_cadena": [],
        "total_por_sucursal": []
    }

def mostrar_reporte_4(resultado):

    print("\n" + "=" * 60)
    print("VENTAS DE PRODUCTOS - CADENA COMPLETA")
    print("=" * 60)

    for fila in resultado["total_cadena"]:

        print(
            f"\nCategoría: {fila['categoria']}"
            f"\nCantidad vendida: {fila['cantidad_total']}"
            f"\nImporte vendido: ${fila['importe_total']:.2f}"
        )

    print("\n" + "=" * 60)
    print("VENTAS DE PRODUCTOS POR SUCURSAL")
    print("=" * 60)

    sucursal_actual = None

    for fila in resultado["total_por_sucursal"]:

        if fila["sucursal"] != sucursal_actual:
            sucursal_actual = fila["sucursal"]

            print(f"\nSucursal: {sucursal_actual}")
            print("-" * 40)

        print(
            f"Categoría: {fila['categoria']} | "
            f"Cantidad: {fila['cantidad_total']} | "
            f"Importe: ${fila['importe_total']:.2f}"
        )

#5. Ranking de monto vendido, agrupado por producto y por sucursal.

def reporte_5():

    pipeline = [


        {
            "$unwind": "$items"
        },

        {
            "$facet": {

                # ======================
                # RANKING CADENA COMPLETA
                # ======================
                "ranking_cadena": [

                    {
                        "$group": {
                            "_id": "$items.producto_id",

                            "monto_total_vendido": {
                                "$sum": {
                                    "$multiply": [
                                        "$items.cantidad",
                                        "$items.precio_unitario"
                                    ]
                                }
                            },

                            "cantidad_total": {
                                "$sum": "$items.cantidad"
                            }
                        }
                    },

                    {
                        "$lookup": {
                            "from": "productos",
                            "localField": "_id",
                            "foreignField": "_id",
                            "as": "producto"
                        }
                    },

                    {
                        "$unwind": "$producto"
                    },

                    {
                        "$project": {
                            "_id": 0,
                            "producto": "$producto.descripcion",
                            "cantidad_total": 1,
                            "monto_total_vendido": 1
                        }
                    },

                    {
                        "$sort": {
                            "monto_total_vendido": -1
                        }
                    }
                ],

                # ======================
                # RANKING POR SUCURSAL
                # ======================
                "ranking_por_sucursal": [

                    {
                        "$group": {
                            "_id": {
                                "sucursal": "$sucursal",
                                "producto": "$items.producto_id"
                            },

                            "monto_total_vendido": {
                                "$sum": {
                                    "$multiply": [
                                        "$items.cantidad",
                                        "$items.precio_unitario"
                                    ]
                                }
                            },

                            "cantidad_total": {
                                "$sum": "$items.cantidad"
                            }
                        }
                    },

                    {
                        "$lookup": {
                            "from": "productos",
                            "localField": "_id.producto",
                            "foreignField": "_id",
                            "as": "producto"
                        }
                    },

                    {
                        "$lookup": {
                            "from": "sucursales",
                            "localField": "_id.sucursal",
                            "foreignField": "_id",
                            "as": "sucursal"
                        }
                    },

                    {
                        "$unwind": "$producto"
                    },

                    {
                        "$unwind": "$sucursal"
                    },

                    {
                        "$project": {
                            "_id": 0,
                            "producto": "$producto.descripcion",
                            "sucursal": "$sucursal.nombre",
                            "cantidad_total": 1,
                            "monto_total_vendido": 1
                        }
                    },

                    {
                        "$sort": {
                            "monto_total_vendido": -1
                        }
                    }
                ]
            }
        }
    ]

    resultado = list(Venta._get_collection().aggregate(pipeline))

    return resultado[0] if resultado else {
        "ranking_cadena": [],
        "ranking_por_sucursal": []
    }

def mostrar_reporte_5(resultado):

    print("\n" + "=" * 70)
    print("RANKING DE PRODUCTOS - CADENA COMPLETA")
    print("=" * 70)

    if resultado["ranking_cadena"]:

        for i, item in enumerate(resultado["ranking_cadena"][:10], start=1):

            print(
                f"{i:2d}. "
                f"{item['producto']} | "
                f"Cantidad: {item['cantidad_total']} | "
                f"Monto: ${item['monto_total_vendido']:,.2f}"
            )

    else:
        print("Sin resultados.")


    print("\n" + "=" * 70)
    print("RANKING DE PRODUCTOS POR SUCURSAL")
    print("=" * 70)

    if resultado["ranking_por_sucursal"]:

        for i, item in enumerate(resultado["ranking_por_sucursal"][:10], start=1):

            print(
                f"{i:2d}. "
                f"Sucursal: {item['sucursal']} | "
                f"Producto: {item['producto']} | "
                f"Cantidad: {item['cantidad_total']} | "
                f"Monto: ${item['monto_total_vendido']:,.2f}"
            )

    else:
        print("Sin resultados.")