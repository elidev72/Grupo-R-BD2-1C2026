
import json
from datetime import datetime

from config import conectar_db, desconectar_db
from models import *

from reportes_ivan import *
from reportes_rodrigo import *
from reportes_eze import *

# IMPORTANTE: si lo usás en 7 y 8
try:
    from utils import MongoEncoder
except:
    MongoEncoder = None


if __name__ == "__main__":
    conectar_db()
    
    salir = False
    while not salir:
        print("\n--- Menu opciones reportes ---")
        print("1- Reporte 1: CANTIDAD DE VENTAS POR CADENA Y SUCURSALES (ENTRE DOS FECHAS)")
        print("2- Reporte 2: OBRAS SOCIALES (ENTRE DOS FECHAS)")
        print("3- Reporte 3: COBRANZA TOTAL Y POR SUCURSALES")
        print("4- Reporte 4")
        print("5- Reporte 5")
        print("6- Reporte 6")
        print("7- Reporte 7")
        print("8- Reporte 8")
        print("9- Salir")

        opcion = int(input("Introduce una opcion: "))

        # -------------------------
        # 📊 REPORTE 1
        # -------------------------
        if opcion == 1:
            print("\n--- REPORTE 1 ---")

            desde = input("Fecha desde (YYYY-MM-DD): ")
            hasta = input("Fecha hasta (YYYY-MM-DD): ")

            resultado = reporte_1(
                datetime.fromisoformat(desde),
                datetime.fromisoformat(hasta)
            )

            print("\n" + "="*80)
            print("RESULTADO REPORTE 1")
            print("="*80)
            print(json.dumps(resultado, indent=2, ensure_ascii=False))
            print("="*80)

        # -------------------------
        # 📊 REPORTE 2
        # -------------------------
        elif opcion == 2:
            try:
                desde = input("Fecha desde (YYYY-MM-DD): ")
                hasta = input("Fecha hasta (YYYY-MM-DD): ")

                resultado = reporte_2(
                    datetime.fromisoformat(desde),
                    datetime.fromisoformat(hasta)
                )

                print(json.dumps(resultado, indent=2, ensure_ascii=False))
            except:
                print("❌ Reporte 2 no disponible o error")

        # -------------------------
        elif opcion == 3:
            try:
                reporte_3()
            except:
                print("❌ Reporte 3 no disponible")

        elif opcion == 4:
            try:
                reporte_4()
            except:
                print("❌ Reporte 4 no disponible")

        elif opcion == 5:
            try:
                reporte_5()
            except:
                print("❌ Reporte 5 no disponible")

        # -------------------------
        elif opcion == 6:
            try:
                reporte_6()
            except:
                print("❌ Reporte 6 no disponible")

        # -------------------------
        elif opcion == 7:
            try:
                ranking = reporte_7()

                if MongoEncoder:
                    print(json.dumps(ranking, cls=MongoEncoder, indent=2, ensure_ascii=False))
                else:
                    print(json.dumps(ranking, indent=2, ensure_ascii=False))

                print(f"\nTotal: {len(ranking)}")
            except:
                print("❌ Reporte 7 no disponible")

        # -------------------------
        elif opcion == 8:
            try:
                ranking = reporte_8()

                if MongoEncoder:
                    print(json.dumps(ranking, cls=MongoEncoder, indent=2, ensure_ascii=False))
                else:
                    print(json.dumps(ranking, indent=2, ensure_ascii=False))

                print(f"\nTotal: {len(ranking)}")
            except:
                print("❌ Reporte 8 no disponible")

        # -------------------------
        elif opcion == 9:
            salir = True

    desconectar_db()
    
    