
import json
from datetime import datetime

from config import conectar_db, desconectar_db
from models import *
from reportes_ivan import *
from reportes_rodrigo import *
from reportes_eze import *


def imprimir_reporte(titulo, data):
    print("\n" + "=" * 80)
    print(titulo)
    print("=" * 80)
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def leer_fecha(mensaje):
    while True:
        try:
            fecha = input(mensaje)
            return datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            print("❌ Formato inválido. Usá YYYY-MM-DD")


def leer_opcion():
    try:
        return int(input("Introduce una opción: "))
    except ValueError:
        return None


if __name__ == "__main__":
    conectar_db()

    salir = False

    while not salir:
        print("\n--- MENÚ DE REPORTES ---")
        print("1- Reporte 1: VENTAS POR CADENA Y SUCURSAL (ENTRE FECHAS)")
        print("2- Reporte 2: VENTAS POR OBRA SOCIAL (ENTRE FECHAS)")
        print("3- Reporte 3: COBRANZA TOTAL Y POR SUCURSAL")
        print("4- Reporte 4: VENTAS POR TIPO DE PRODUCTO")
        print("5- Reporte 5: RANKING MONTO VENDIDO POR PRODUCTO Y SUCURSAL")
        print("6- Reporte 6: RANKING CANTIDAD PRODUCTOS VENDIDOS")
        print("7- Reporte 7: RANKING CLIENTES CADENA")
        print("8- Reporte 8: RANKING CLIENTES INTRA-SUCURSAL")
        print("9- Salir")

        opcion = leer_opcion()

        if opcion is None:
            print("❌ Opción inválida")
            continue

        # -------------------- REPORTE 1 --------------------
        if opcion == 1:
            fecha_desde = leer_fecha("Fecha desde (YYYY-MM-DD): ")
            fecha_hasta = leer_fecha("Fecha hasta (YYYY-MM-DD): ")

            resultado = reporte_1(fecha_desde, fecha_hasta)
            imprimir_reporte("REPORTE 1: VENTAS POR CADENA Y SUCURSAL", resultado)

        # -------------------- REPORTE 2 --------------------
        elif opcion == 2:
            try:
                fecha_desde = leer_fecha("Fecha desde (YYYY-MM-DD): ")
                fecha_hasta = leer_fecha("Fecha hasta (YYYY-MM-DD): ")

                resultado = reporte_2(fecha_desde, fecha_hasta)
                imprimir_reporte("REPORTE 2: VENTAS POR OBRA SOCIAL", resultado)

            except Exception as e:
                print("❌ Error en Reporte 2:", e)

        # -------------------- REPORTE 3 --------------------
        elif opcion == 3:
           try:
                fecha_inicio = datetime(2026, 1, 1)
                fecha_fin = datetime(2026, 12, 31)
                resultado = reporte_3(fecha_inicio, fecha_fin)
                mostrar_reporte_3(resultado)
           except Exception as e:
                print(f"Error al generar el reporte 3: {e}")

        elif opcion == 4:
            try:
                fecha_inicio = datetime(2026, 1, 1)
                fecha_fin = datetime(2026, 12, 31)
                resultado = reporte_4(fecha_inicio, fecha_fin)
                mostrar_reporte_4(resultado)
            except Exception as e:
                print(f"Error al generar el reporte 4: {e}")
        elif opcion == 5:
            try:
                fecha_inicio = datetime(2026, 1, 1)
                fecha_fin = datetime(2026, 12, 31)
                resultado = reporte_5(fecha_inicio, fecha_fin)
                mostrar_reporte_5(resultado)
            except Exception as e:
                print(f"Error al generar el reporte 5: {e}")
        elif opcion == 6:
            try:
                resultado = reporte_6()
                imprimir_reporte("REPORTE 6: RANKING PRODUCTOS VENDIDOS", resultado)
            except Exception as e:
                print("❌ Error en Reporte 6:", e)

        # -------------------- REPORTE 7 --------------------
        elif opcion == 7:
            try:
                ranking = reporte_7()
                imprimir_reporte("REPORTE 7: CLIENTES CADENA", ranking)
                print(f"\nTotal clientes activos: {len(ranking)}")
            except Exception as e:
                print("❌ Error en Reporte 7:", e)

        # -------------------- REPORTE 8 --------------------
        elif opcion == 8:
            try:
                ranking = reporte_8()
                imprimir_reporte("REPORTE 8: CLIENTES INTRA-SUCURSAL", ranking)
                print(f"\nTotal registros: {len(ranking)}")
            except Exception as e:
                print("❌ Error en Reporte 8:", e)

        # -------------------- SALIR --------------------
        elif opcion == 9:
            salir = True
            print("Saliendo del sistema...")

        else:
            print("❌ Opción fuera de rango")

    desconectar_db()
    
    
    
    