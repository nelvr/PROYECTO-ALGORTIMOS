import numpy as np 
import random 
import colorama 
from colorama import * 
from enum import Enum
import re 
init(autoreset=True)

# Arreglos y matrices 
m = np.full((0,0),0)
n = np.full((0,0),0)

# Declaracion de variables globales
region_actual = None
x = 0
epicentro = None
afectadas = None 

# Clases 
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

# Funciones y procedimientos
def cargar_archivo():
    global m, n
    with open(r"E:\terremoto\entra.txt","rt") as f: 
        lineas = f.readlines()
        header = lineas[0].strip()
        match = re.match(r'\*\s*(\d+)\s+(.+)', header)
        if not match: 
            print("Formato invalido en la primera linea del codigo")
            return None 
        numero_region = int(match.group(1))
        nombre_region = match.group(2).strip()
        m, n = map(int,lineas[1].strip().split())
        if not (5 <= m <= 20) or not (5 <= n <= 20):
            print("Dimensiones fuera del rango (5-20)")
            return None
        costos = np.full((m, n),0)  
        for i in range(m):
            fila = lineas[2 + i].strip().split()
            for j in range(n):
                costos[i][j] = int(fila[j]) 
        print("Matriz de costos:")
        print(costos) 
        perdidas = np.full((m,n),0)
        for i in range(m):
            fila2 = lineas[2+m+i].strip().split()
            for j in range(n):
                perdidas[i][j] = int(fila2[j])
        print("\nMatriz de pérdidas:")
        print(perdidas)

        print(f"\nCargada región '{nombre_region}' ({m}x{n})")
        return {'nombre': nombre_region, 'region': numero_region, 'M': m, 'N': n, 'costo': costos, 'perdidas': perdidas}

def entrada_manual():
    global m, n
    print("Carga Manual..")
    m = int(input("Filas (5-20): "))
    n = int(input("Columnas (5-20): "))
    if not (5 <= m <= 20 and 5 <= n <= 20):
        print("Dimensiones inválidas.")
        return None
    else:
        numero_region = random.randint(1,9)
        costos = np.full((m,n),0)
        perdidas = np.full((m,n),0)
        for i in range(m):
            for j in range(n):
                costos[i,j] = random.randint(10,99)
                perdidas[i,j] = random.randint(10,99)  
        print(f"Carga manual exitosa, ({m}x{n})")          
        input("Pulse cualquier tecla para continuar: ")
        return {'nombre': f"Región {numero_region}", 'region': numero_region, 'M': m, 'N': n, 'costo': costos, 'perdidas': perdidas}

def Modificar(region):
    if region is None:
        print("Primero debe cargar una región")
        return region
    
    m = region['M']
    n = region['N']
    print("Ingrese coordenadas i,j a modificar o -1 para salir.")
    i = int(input("Fila: "))
    j = int(input("Columna: "))
    if i == -1 and j == -1:
        print("Volviendo al menu..")
        input("Pulse cualquier tecla para continuar: ")
        return region
    
    if 0 <= i < m and 0 <= j < n:
        print(f"Costo actual: {region['costo'][i,j]}")
        nuevo_costo = int(input("Nuevo costo economico: "))
        region['costo'][i,j] = nuevo_costo
        print(f"Pérdida actual: {region['perdidas'][i,j]}")
        nueva_perdida = int(input("Nueva pérdida: "))
        region['perdidas'][i,j] = nueva_perdida
        print("Celda modificada correctamente..")
    else:
        print("Coordenadas ingresadas incorrectamente")
        print("Intente nuevamente..")
    
    input("Pulse cualquier tecla para continuar: ")
    return region

def Consecuencias():
    global m, n
    if m == 0 or n == 0:
        print("Primero debe cargar una región")
        return
    
    i = int(input(f'Epicentro - Fila i (0 a {m-1}): '))
    j = int(input(f'Epicentro - Columna j (0 a {n-1}): '))
    g = int(input("Ingrese la intensidad del terremoto (1-7): "))
    if not (0 <= i < m and 0 <= j < n and 1 <= g <= 7):
        print("Epicentro o intensidad invalida.")
        return
    print(f"Consecuencias calculadas para epicentro ({i},{j}) con intensidad {g}")

def main():
    global region_actual, m, n
    
    # Programa Principal
    print("Proyecto Terremoto CERT ")
    print(Fore.BLUE + "UCAB Elaborado por Adrian Garcia, Nelson Villaroel y Gabriel Chiquito")
    
    while True:
        print(Fore.BLACK + """                   MENU CERT 
                1.- Carga o Modificacion de costos economicos y perdidas humanas
                2.- estimacion de las consecuencias de un terremoto 
                3.- estimacion de la zona maximo y minimo riesgo 
                4.- mostrar la region geografica 
                5.- Salir""")
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("Por favor, ingrese un número válido.")
            continue
            
        if opcion == 1: 
            print("\n------ Submenú carga/modificación ------")
            print("1. Cargar desde archivo ENTRA.TXT")
            print("2. Carga MANUAL (pedir cada celda)")
            print("3. Modificar unidad individual")
            print("4. Volver al menú principal")
            try:
                so = int(input("Elija subopción: "))
            except ValueError:
                print("Opción inválida")
                continue
                
            if so == 1:
                region_actual = cargar_archivo()
            elif so == 2: 
                region_actual = entrada_manual()
            elif so == 3:
                region_actual = Modificar(region_actual)
            elif so == 4: 
                print("Volviendo al menu principal....")
            else:
                print("Opción no válida")
                
        elif opcion == 2: 
            Consecuencias()
        elif opcion == 3:
            g = int(input("Ingrese la intensidad de grados (1-7) del terremoto: "))
            if g < 1 or g > 7:
                print("ERROR, intente nuevamente.")
                print("Debe ingresar la intensidad del (1-7)")
            else: 
                print("Calculando epicentro..")
                input("Pulse cualquier tecla para continuar: ")
        elif opcion == 4:
            if region_actual:
                print(f"Región actual: {region_actual['nombre']}")
                print(f"Dimensiones: {region_actual['M']}x{region_actual['N']}")
            else:
                print("No hay región cargada")
        elif opcion == 5:
            print("Gracias por utilizar el Programa CERT!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
main()