import numpy as np 
import random 
import colorama 
from colorama import * 
init(autoreset=True)
from enum import Enum
import re 
def main():
    # Arreglos y matrices 
    m = np.full((0,0),0)
    n = np.full((0,0),0)
    #Declaracion de variables globales
    m:int 
    n:int 
    m= 0 
    n = 0 
    region_actual = None
    x:int 
    epicentro = None
    afectadas = None 
    
    #Clases 
    class RegionGeografica(Enum):
        CORDILLERA_CENTRAL      = (1, "Cordillera Central")
        CORDILLERA_ORIENTAL     = (2, "Cordillera Oriental")
        SISTEMA_CORIANO         = (3, "Sistema Coriano")
        LAGO_DE_MARACAIBO       = (4, "Lago de Maracaibo")
        LOS_ANDES               = (5, "Los Andes")
        LOS_LLANOS              = (6, "Los Llanos")
        SISTEMA_DELTAICO        = (7, "Sistema Deltáico")
        SUR_ORINOCO_GUAYANA     = (8, "Sur del Orinoco: La Guayana")
        LAS_ISLAS               = (9, "Las Islas: Nueva Esparta y Dependencias Federales")

    #Funciones y procedimientos
    def cargar_archivo():
        nonlocal m,n 
        with open(r"E:\terremoto\entra.txt","rt") as f: 
            lineas = f.readlines()
        header = lineas[0].strip()
        match = re.match(r'\*\s*(\d+)\s+(.+)', header)
        if not match: 
            print("Formato invalido en la primera linea del codigo")
            return None 
        numero_region= int(match.group(1))
        nombre_region=match.group(2).strip()
        m,n = map(int,lineas[1].strip().split())
        if (5 < m > 20) or (5 < n > 20):
            print("Dimensiones fuera del rango (5-20)")
        costos = np.full((m, n),0)  
        for i in range(m):
            fila = lineas[2 + i].strip().split()
            for j in range(n):
                costos[i][j] = int(fila[j]) 
        print(costos,end=" ") 
        print() 
        perdidas= np.full((m,n),0)
        for i in range(m):
            fila2 = lineas[2+m+i].strip().split()
            for j in range(n):
                perdidas[i][j] = int(fila2[j])
        print(perdidas)
        print()

        print(f"Cargada región '{nombre_region}' ({m}x{n})")
        return {'nombre': nombre_region, 'region': numero_region, 'M': m, 'N': n, 'costo': costos, 'perdidas': perdidas}

    def entrada_manual(m,n):
        print("Carga Manual..")
        m = int(input("Filas (5-20): "))
        n = int(input("Columnas (5-20): "))
        if not (5 <= m <= 20 and 5 <= n <= 20):
            print("Dimensiones inválidas.")
        else:
            numero_region=random.randint(1,9)
            costos = np.full((m,n),0)
            perdidas = np.full((m,n),0)
            for i in range(m):
                for j in range(n):
                    costos[i,j]=random.randint(10,99)
                    perdidas[i,j]=random.randint(10,99)  
            print(f"Carga manual exitosa, *({m}x{n})")          
            omitir = input("Pulse cualquier tecla para continuar: ")
            
    def Modificar(region):
        m = region['M']
        n = region['N']
        print("Ingrese coordenadas i,j a modificar o -1 para salir.")
        i = int(input("Fila: "))
        j = int(input("Columna: "))
        if i == -1 and j == -1:
            print("Volviendo al menu..")
            omitir = input("Pulse cualquier tecla para continuar: ")
            return opcion 
        if 0 <= i < m and 0<=j<n:
            print(f"Costo actual:{region['costo'][i,j]}")
            nuevo_costo = int(input("Nuevo costo economico: "))
            costo = region['costo'][i,j]
            print(f"Perdida actual: {region['perdidas'][i,j]}")
            nueva_perdida = int(input("Nueva perdidas: "))
            perdida = region['perdidas'][i,j]
            print("Celda modificada correctamente..")
        else:
            print("Coordenadas ingresadas incorrectamente")
            print("Intente nuevamente..")
        
    def Consecuencias():
        i = int(input(f'Epicentro - Fila i (0 a {m-1}): '))
        j = int(input(f'Epicentro - Columna j (0 a {n-1}): '))
        g = int(input("Ingrese la intensidad del terrmoto del (1-7):"))
        if not (0 <= i < m and 0 <= j < n and 1 <= g <= 7):
            print("Epicentro o intensidad invalida.")
        

    #Programa Principal
    print("Proyecto Terremoto CERT ")
    print(Fore.BLUE+"UCAB Elaborado por Adrian Garcia,Nelson Villaroel y Gabriel Chiquito")
    while True:
        print(Fore.BLACK+"""                   MENU CERT 
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
               region_actual = cargar_archivo()
            if so == 2: 
                region_actual = entrada_manual(m,n)
            if so == 3:
                Modificar(region_actual)
            if so == 4: 
                print("Volviendo al menu principal....")
        if opcion == 2: 
            Consecuencias()
        if opcion == 3:
            g = int(input("Ingrese la intensidad de grados (1-7) del terremoto:  "))
            if g < 1 or g > 7:
                print("ERROR, intentenuevamente.")
                print("Debe ingresar la intensidad del (1-7)")
            else: 
                print("Calculando epicentro..")
                omitir = input("Pulse cualquier tecla para continuar: ")
                print("a")
        if opcion == 5:
            print("Gracias por utilizar el Programa CERT!")
            return False 
main()
