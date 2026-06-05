
from models import Venta, Persona, Sucursal

#7. Ranking compras agrupadas por cliente para el total de la cadena. (quiero ver los clientes
#que mas compraron en toda la cadena, pudieron comprar en mas de una sucursal)

def reporte_7():
    """
    Ranking de clientes por cantidad total de compras en toda la cadena.
    
    """
    pipeline = [
        # Desagrupar items para contar cada uno correctamente
        {"$unwind": "$items"},
        # Agrupar por cliente, sumando cantidades y montos
        {
            "$group": {
                "_id": "$cliente",
                "total_cantidad": {"$sum": "$items.cantidad"},
                "total_monto": {"$sum": {"$multiply": ["$items.cantidad", "$items.precio_unitario"]}}
            }
        },
        # Ordenar descendente por cantidad
        {"$sort": {"total_monto":-1}}
    ]
    
    resultados = list(Venta._get_collection().aggregate(pipeline))
    
    if not resultados:
        print("No hay ventas registradas")
        return []
    
    # Obtener información de clientes en bulk usando ObjectIds directamente
    cliente_ids = [r["_id"] for r in resultados]
    clientes = {p.pk: p for p in Persona.objects(pk__in=cliente_ids)}
    
    # Construir ranking con información completa
    ranking = []
    for idx, resultado in enumerate(resultados, 1):
        cliente = clientes.get(resultado["_id"])
        
        ranking.append({
            "ranking": idx,
            "cliente_id": str(resultado["_id"]),
            "dni": cliente.dni if cliente else "N/A",
            "nombre": cliente.nombre if cliente else "N/A",
            "apellido": cliente.apellido if cliente else "N/A",
            "cantidad_items_comprados": resultado["total_cantidad"],
            "monto_total": round(resultado["total_monto"], 2)
        })
    

    
    return ranking


#8. Ranking compras agrupadas por cliente y por sucursal. (quiero ver como compraron los
#clientes intra-sucursal)

def reporte_8():
    """
    Ranking de clientes por cantidad de compras, desglosado por sucursal.
    
    Métrica principal: cantidad total de items comprados POR CLIENTE Y SUCURSAL
    Métrica secundaria: monto total invertido por cliente en esa sucursal
    
    Un mismo cliente puede aparecer múltiples veces (una por cada sucursal donde compró)
    Retorna: Lista de dicts con ranking ordenado descendente
    """
    pipeline = [
        # Desagrupar items para contar cada uno correctamente
        {"$unwind": "$items"},
        # Agrupar por cliente Y sucursal
        {
            "$group": {
                "_id": {
                    "cliente": "$cliente",
                    "sucursal": "$sucursal"
                },
                "total_cantidad": {"$sum": "$items.cantidad"},
                "total_monto": {"$sum": {"$multiply": ["$items.cantidad", "$items.precio_unitario"]}}
            }
        },
        # Ordenar descendente por cantidad
        {"$sort": {"total_cantidad": -1}}
    ]
    
    resultados = list(Venta._get_collection().aggregate(pipeline))
    
    if not resultados:
        print("No hay ventas registradas")
        return []
    
    # Obtener información de clientes y sucursales en bulk usando ObjectIds directamente
    cliente_ids = [r["_id"]["cliente"] for r in resultados]
    sucursal_ids = [r["_id"]["sucursal"] for r in resultados]
    
    clientes = {p.pk: p for p in Persona.objects(pk__in=cliente_ids)}
    sucursales = {s.pk: s for s in Sucursal.objects(pk__in=sucursal_ids)}
    
    # Construir ranking con información completa
    ranking = []
    for idx, resultado in enumerate(resultados, 1):
        cliente = clientes.get(resultado["_id"]["cliente"])
        sucursal = sucursales.get(resultado["_id"]["sucursal"])
        
        ranking.append({
            "ranking": idx,
            "cliente": {
                "cliente_id": str(resultado["_id"]["cliente"]),
                "dni": cliente.dni if cliente else "N/A",
                "nombre": cliente.nombre if cliente else "N/A",
                "apellido": cliente.apellido if cliente else "N/A"
            },
            "sucursal": {
                "sucursal_id": str(resultado["_id"]["sucursal"]),
                "nombre": sucursal.nombre if sucursal else "N/A",
                "ubicacion": {
                    "calle": sucursal.sede.calle if sucursal else "N/A",
                    "numero": sucursal.sede.numero if sucursal else "N/A",
                    "localidad": sucursal.sede.localidad if sucursal else "N/A",
                    "provincia": sucursal.sede.provincia if sucursal else "N/A"
                } if sucursal else None
            },
            "cantidad_items_comprados": resultado["total_cantidad"],
            "monto_total": round(resultado["total_monto"], 2)
        })
    
    return ranking