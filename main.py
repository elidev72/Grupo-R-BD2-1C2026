import json
from datetime import datetime

from config import conectar_db, desconectar_db
from models import *
from reportes_ivan import *
from reportes_rodrigo import *
from reportes_eze import *

if __name__ == "__main__":
    conectar_db()

    salir = False
    while not salir:
        print("--- Menu opciones reportes ---")
        print("1- Reporte 1: CANTIDAD DE VENTAS POR CADENA Y SUCURSALES (ENTRE DOS FECHAS)")
        print("2- Reporte 2: CANTIDADES DE VENTAS AGRUPADAS POR OBRAS SOCIALES (ENTRE DOS FECHAS)")
        print("3- Reporte 3: COBRANZA TOTAL Y POR SUCURSALES (ENTRE DOS FECHAS)")
        print("4- Reporte 4: CANTIDADES DE VENTAS POR TIPO DE PRODUCTO (ENTRE DOS FECHAS)")
        print("5- Reporte 5: RANKING DE MONTO VENDIDO POR PRODUCTO Y SUCURSAL")
        print("6- Reporte 6: RANKING DE CANTIDAD DE PRODUCTOS VENDIDOS POR PRODUCTO Y SUCURSAL")
        print("7- Reporte 7: RANKING DE CLIENTES POR COMPRAS EN TODA LA CADENA")
        print("8- Reporte 8: RANKING DE CLIENTES POR COMPRAS INTRA-SUCURSAL")
        print("9- Salir")

        opcion = int(input("Introduce una opcion: "))

        # -------------------- REPORTE 1 --------------------
        if opcion == 1:
            print("\nIngrese fechas (formato YYYY-MM-DD)")
            fecha_desde = input("Fecha desde: ")
            fecha_hasta = input("Fecha hasta: ")

            fecha_desde = datetime.strptime(fecha_desde, "%Y-%m-%d")
            fecha_hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d")

            resultado = reporte_1(fecha_desde, fecha_hasta)

            print("\n" + "="*80)
            print("REPORTE 1: VENTAS POR CADENA Y SUCURSAL")
            print("="*80)

            print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))

        # -------------------- REPORTE 2 (ARREGLADO) --------------------
        elif opcion == 2:
            try:
                print("\nIngrese fechas (formato YYYY-MM-DD)")
                fecha_desde = input("Fecha desde: ")
                fecha_hasta = input("Fecha hasta: ")

                fecha_desde = datetime.strptime(fecha_desde, "%Y-%m-%d")
                fecha_hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d")

                resultado = reporte_2(fecha_desde, fecha_hasta)

                print("\n" + "="*80)
                print("REPORTE 2: VENTAS POR OBRA SOCIAL")
                print("="*80)

                print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))

            except Exception as e:
                print("\n❌ Error en Reporte 2:", e)

        # -------------------- REPORTE 3 --------------------
        elif opcion == 3:
            try:
                reporte_3()
            except Exception as e:
                print("\n❌ Error en Reporte 3:", e)

        # -------------------- REPORTE 4 --------------------
        elif opcion == 4:
            try:
                reporte_4()
            except Exception as e:
                print("\n❌ Error en Reporte 4:", e)

        # -------------------- REPORTE 5 --------------------
        elif opcion == 5:
            try:
                reporte_5()
            except Exception as e:
                print("\n❌ Error en Reporte 5:", e)

        # -------------------- REPORTE 6 (MEJORADO) --------------------
        elif opcion == 6:
            try:
                resultado = reporte_6()

                print("\n" + "="*80)
                print("REPORTE 6: RANKING DE PRODUCTOS VENDIDOS")
                print("="*80)

                print(json.dumps(resultado, indent=2, ensure_ascii=False, default=str))

            except Exception as e:
                print("\n❌ Error en Reporte 6:", e)

        # -------------------- REPORTE 7 --------------------
        elif opcion == 7:
            try:
                ranking = reporte_7()

                print("\n" + "="*80)
                print("REPORTE 7: RANKING DE CLIENTES POR COMPRAS EN TODA LA CADENA")
                print("="*80)

                print(json.dumps(ranking, indent=2, ensure_ascii=False, default=str))
                print(f"\nTotal de clientes activos: {len(ranking)}")

            except Exception as e:
                print("\n❌ Error en Reporte 7:", e)

        # -------------------- REPORTE 8 --------------------
        elif opcion == 8:
            try:
                ranking = reporte_8()

                print("\n" + "="*80)
                print("REPORTE 8: RANKING DE CLIENTES POR COMPRAS INTRA-SUCURSAL")
                print("="*80)

                print(json.dumps(ranking, indent=2, ensure_ascii=False, default=str))
                print(f"\nTotal de combinaciones cliente-sucursal: {len(ranking)}")

            except Exception as e:
                print("\n❌ Error en Reporte 8:", e)

        # -------------------- SALIR --------------------
        elif opcion == 9:
            salir = True

    desconectar_db()
    
    
    