import numpy as np 
import random 
import colorama 
from enum import Enum
def main():
    # Arreglos y matrices 
    M = np.full((6,6),9)
    N = np.full((6,6),9)
    #Declaracion de variables globales
    file = "ENTRA.txt"
    #Clases 
    class Regiones(Enum):
        CORDILLERA_CENTRAL=1 
        CORDILLERA_ORIENTAL=2
        SISTEMA_CORIANO=3
        LAGO_DE_MARACAIBO=4
        LOS_ANDES=5
        LOS_LLANOS=6
        SISTEMA_DELTAICO=7
        SUR_DEL_ORINOCO=8
        ISLAS=9 
    #Funciones y procedimientos
    def Archivo(path):
        arch = open(path,"rt")
        l1 = arch.readline().split(" ")
        l2 = arch.readline().split(" ")

    #Programa Principal
    print("Proyecto Terremoto CERT ")
    print("""""UCAB Elaborado por Adrian Garcia 
        Gabriel Chiquito
        Nelson """)
    
    while True:
        print("""                   MENU CERT 
            1.- Carga o Modificacion de costos economicos y perdidas humanas
            2.- estimacion de las consecuencias de un terremoto 
            3.- estimacion de la zona maximo y minimo riesgo 
            4.- mostrar la region geografica 
            5.- Salir""")
        opcion = int(input())
        if opcion == 1: 
            print("\n------ Submenú carga/modificación ------")
            print("1. Cargar desde archivo ENTRA.TXT")
            print("2. Carga MANUAL (pedir cada celda)")
            print("3. Modificar unidad individual")
            print("4. Volver al menú principal")
            so = int(input("Elija subopción: "))
            if so == 1:
                print()
            if so == 2: 
                print()
            if so == 3:
                print()
            if so == 4: 
                print("Volviendo al menu principal....")
        if opcion == 2: 
            print("A continuacion")
            print("Va ingresar las coordenadas del epicentro")
            M = int(input("Fila i: "))
            N = int(input("Columna j: "))
        if opcion == 3:
            g = int(input("Ingrese la intensidad de grados (1-7) del terremoto:  "))
            if g < 1 or g > 7:
                print("ERROR, intentenuevamente.")
                print("Debe ingresar la intensidad del (1-7)")
            else: 
                print("s")
        if opcion == 5:
            print("Gracias por utilizar el Programa!")
            return False 

    

main()