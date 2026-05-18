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
        print("1- Reporte 1")
        print("2- Reporte 2")
        print("3- Reporte 3")
        print("4- Reporte 4")
        print("5- Reporte 5")
        print("6- Reporte 6")
        print("7- Reporte 7")
        print("8- Reporte 8")
        print("9- Salir")

        opcion = int(input("Introduce una opcion: "))

        if opcion == 1:
            reporte_1()
        elif opcion == 2:
            reporte_2()
        elif opcion == 3:
            reporte_3()
        elif opcion == 4:
            reporte_4()
        elif opcion == 5:
            reporte_5()
        elif opcion == 6:
            reporte_6()
        elif opcion == 7:
            reporte_7()
        elif opcion == 8:
            reporte_8()
        elif opcion == 9:
            salir = True

    desconectar_db()
