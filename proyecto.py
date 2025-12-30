import numpy as np 
import random 
import colorama 
from colorama import * 
from enum import Enum
import re 
import os

init(autoreset=True)

# Arreglos y matrices 
m = np.full((0,0),0)
n = np.full((0,0),0)

# Declaracion de variables globales
region_actual = None
ultimo_epicentro = None
ultimo_grado = None
ultimo_afectadas = None

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

# ========== FUNCIONES NUEVAS/MEJORADAS ==========

def calcular_impacto(region, epi_i, epi_j, grado):
    """Calcula el impacto total de un terremoto usando distancia Manhattan"""
    if region is None:
        return 0, 0, None
    
    M = region['M']
    N = region['N']
    costos = region['costo']
    perdidas = region['perdidas']
    
    total_costo = 0
    total_fallecidos = 0
    matriz_afectados = np.full((M, N), False)
    
    for i in range(M):
        for j in range(N):
            distancia = abs(i - epi_i) + abs(j - epi_j)
            if distancia <= grado:
                total_costo += costos[i, j]
                total_fallecidos += perdidas[i, j]
                matriz_afectados[i, j] = True
    
    return total_costo, total_fallecidos, matriz_afectados

def buscar_zonas_riesgo(region, grado):
    """Encuentra epicentros con mayor y menor impacto"""
    if region is None:
        return None, None, None, None
    
    M = region['M']
    N = region['N']
    
    mayor_impacto = -1
    menor_impacto = float('inf')
    pos_mayor = (0, 0)
    pos_menor = (0, 0)
    
    for i in range(M):
        for j in range(N):
            costo, fallecidos, _ = calcular_impacto(region, i, j, grado)
            impacto_total = costo + fallecidos
            
            if impacto_total > mayor_impacto:
                mayor_impacto = impacto_total
                pos_mayor = (i, j)
            
            if impacto_total < menor_impacto:
                menor_impacto = impacto_total
                pos_menor = (i, j)
    
    # Convertir a 1-based para mostrar al usuario
    pos_mayor_1based = (pos_mayor[0] + 1, pos_mayor[1] + 1)
    pos_menor_1based = (pos_menor[0] + 1, pos_menor[1] + 1)
    
    return pos_mayor_1based, mayor_impacto, pos_menor_1based, menor_impacto

def mostrar_region_completa(region, epicentro=None, grado=None, matriz_afectados=None):
    """Muestra la región de forma legible y con emojis"""
    if region is None:
        print("No hay región cargada")
        return
    
    M = region['M']
    N = region['N']
    costos = region['costo']
    perdidas = region['perdidas']
    
    print("\n" + "="*60)
    print(f"REGIÓN: {region['nombre']} ({M}x{N})")
    print("="*60)
    
    # Mostrar de forma legible
    print("\n" + Fore.CYAN + "DATOS DE LA REGIÓN (Costo | Pérdidas):" + Style.RESET_ALL)
    print(" " * 5 + " ".join([f"{j+1:^10}" for j in range(N)]))
    print(" " * 5 + "-" * (N * 11))
    
    for i in range(M):
        fila_str = f"{i+1:3} | "
        for j in range(N):
            # Marcar epicentro
            if epicentro and (i+1, j+1) == epicentro:
                celda = f"[{costos[i,j]:2}|{perdidas[i,j]:2}]"
                celda = Fore.RED + Back.YELLOW + celda + Style.RESET_ALL
            # Marcar celdas afectadas
            elif matriz_afectados is not None and matriz_afectados[i, j]:
                celda = f"({costos[i,j]:2}|{perdidas[i,j]:2})"
                celda = Fore.YELLOW + celda + Style.RESET_ALL
            else:
                celda = f" {costos[i,j]:2}|{perdidas[i,j]:2} "
            fila_str += celda + " "
        print(fila_str)
    
    # Mostrar con emojis
    print("\n" + Fore.CYAN + "REPRESENTACIÓN GRÁFICA CON EMOJIS:" + Style.RESET_ALL)
    print("🟩: Costo bajo (<30)  🟨: Costo medio (30-60)  🟥: Costo alto (>60)")
    print("⭐: Epicentro")
    
    for i in range(M):
        for j in range(N):
            # Marcar epicentro
            if epicentro and (i+1, j+1) == epicentro:
                print("⭐", end=" ")
            # Marcar según costo económico
            else:
                costo = costos[i, j]
                if costo < 30:
                    print("🟩", end=" ")
                elif costo < 60:
                    print("🟨", end=" ")
                else:
                    print("🟥", end=" ")
        print()
    
    print("="*60)

# ========== FUNCIONES EXISTENTES MODIFICADAS ==========

def cargar_archivo():
    global region_actual
    try:
        # Verificar si el archivo existe
        if not os.path.exists("ENTRA.TXT"):
            print(Fore.RED + "Error: No se encontró el archivo ENTRA.TXT" + Style.RESET_ALL)
            print("Asegúrate de que el archivo esté en la misma carpeta que el programa.")
            input("Presiona Enter para continuar...")
            return None
        
        with open("ENTRA.TXT", "r", encoding='utf-8') as f: 
            lineas = [linea.strip() for linea in f if linea.strip()]
            
            if not lineas:
                print("Archivo vacío")
                return None
                
            # Línea 1: * número nombre
            header = lineas[0]
            match = re.match(r'\*\s*(\d+)\s+(.+)', header)
            if not match: 
                print("Formato inválido en la primera línea")
                return None 
            
            numero_region = int(match.group(1))
            nombre_region = match.group(2).strip()
            
            # Línea 2: M N
            if len(lineas) < 2:
                print("Archivo incompleto")
                return None
                
            M, N = map(int, lineas[1].split())
            
            if not (5 <= M <= 20) or not (5 <= N <= 20):
                print("Dimensiones fuera del rango (5-20)")
                return None
            
            # Verificar que haya suficientes líneas
            lineas_necesarias = 2 + M * 2
            if len(lineas) < lineas_necesarias:
                print(f"Archivo incompleto. Se esperaban {lineas_necesarias} líneas")
                return None
            
            # Leer costos
            costos = []
            for i in range(M):
                fila = list(map(int, lineas[2 + i].split()))
                if len(fila) != N:
                    print(f"Error: Fila {i+1} de costos no tiene {N} columnas")
                    return None
                costos.append(fila)
            
            # Leer pérdidas humanas
            perdidas = []
            for i in range(M):
                fila = list(map(int, lineas[2 + M + i].split()))
                if len(fila) != N:
                    print(f"Error: Fila {i+1} de pérdidas no tiene {N} columnas")
                    return None
                perdidas.append(fila)
            
            # Convertir a numpy arrays
            costos_array = np.array(costos, dtype=int)
            perdidas_array = np.array(perdidas, dtype=int)
            
            print(Fore.GREEN + f"\n✓ Región cargada exitosamente: '{nombre_region}' ({M}x{N})" + Style.RESET_ALL)
            print(f"  Costos: {M}x{N} | Pérdidas: {M}x{N}")
            
            region_data = {
                'nombre': nombre_region,
                'region': numero_region,
                'M': M,
                'N': N,
                'costo': costos_array,
                'perdidas': perdidas_array
            }
            
            input("\nPresiona Enter para continuar...")
            return region_data
            
    except FileNotFoundError:
        print(Fore.RED + "Error: No se encontró el archivo ENTRA.TXT" + Style.RESET_ALL)
    except ValueError as e:
        print(Fore.RED + f"Error en formato de datos: {e}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error inesperado: {e}" + Style.RESET_ALL)
    
    input("\nPresiona Enter para continuar...")
    return None

def entrada_manual():
    print("="*50)
    print("CARGA MANUAL DE REGIÓN")
    print("="*50)
    
    try:
        M = int(input("Filas (5-20): "))
        N = int(input("Columnas (5-20): "))
        
        if not (5 <= M <= 20) or not (5 <= N <= 20):
            print("Dimensiones fuera del rango (5-20)")
            return None
        
        # Mostrar lista de regiones
        print("\nSeleccione el número de región:")
        for region in RegionGeografica:
            print(f"  {region.value[0]}. {region.value[1]}")
        
        numero_region = int(input("\nNúmero de región (1-9): "))
        if not (1 <= numero_region <= 9):
            print("Número de región inválido")
            return None
        
        # Obtener nombre de región
        nombre_region = RegionGeografica(numero_region).value[1]
        
        # Generar datos aleatorios
        costos = np.random.randint(10, 100, size=(M, N))
        perdidas = np.random.randint(10, 100, size=(M, N))
        
        print(Fore.GREEN + f"\n✓ Región creada exitosamente: '{nombre_region}' ({M}x{N})" + Style.RESET_ALL)
        print("  Datos generados aleatoriamente (10-99)")
        
        region_data = {
            'nombre': nombre_region,
            'region': numero_region,
            'M': M,
            'N': N,
            'costo': costos,
            'perdidas': perdidas
        }
        
        input("\nPresiona Enter para continuar...")
        return region_data
        
    except ValueError:
        print("Error: Ingrese valores numéricos válidos")
        input("Presiona Enter para continuar...")
        return None

def Modificar(region):
    if region is None:
        print("Primero debe cargar una región")
        return region
    
    print("\n" + "="*50)
    print("MODIFICAR CELDA INDIVIDUAL")
    print("="*50)
    
    M = region['M']
    N = region['N']
    
    try:
        print(f"\nDimensiones: {M}x{N} (Ingrese 0 para salir)")
        i = int(input("Fila (1 a {}): ".format(M)))
        j = int(input("Columna (1 a {}): ".format(N)))
        
        if i == 0 or j == 0:
            print("Volviendo al menú...")
            return region
        
        if 1 <= i <= M and 1 <= j <= N:
            # Convertir a 0-based
            i_idx = i - 1
            j_idx = j - 1
            
            print(f"\nValores actuales en [{i},{j}]:")
            print(f"  Costo económico: {region['costo'][i_idx, j_idx]}")
            print(f"  Pérdidas humanas: {region['perdidas'][i_idx, j_idx]}")
            print("-" * 30)
            
            nuevo_costo = int(input("Nuevo costo económico (10-99): "))
            if not (10 <= nuevo_costo <= 99):
                print("Costo fuera de rango, usando valor actual")
                nuevo_costo = region['costo'][i_idx, j_idx]
            
            nueva_perdida = int(input("Nueva pérdida humana (10-99): "))
            if not (10 <= nueva_perdida <= 99):
                print("Pérdida fuera de rango, usando valor actual")
                nueva_perdida = region['perdidas'][i_idx, j_idx]
            
            region['costo'][i_idx, j_idx] = nuevo_costo
            region['perdidas'][i_idx, j_idx] = nueva_perdida
            
            print(Fore.GREEN + "✓ Celda modificada correctamente" + Style.RESET_ALL)
        else:
            print("Coordenadas fuera de rango")
    except ValueError:
        print("Error: Ingrese valores numéricos válidos")
    
    input("\nPresiona Enter para continuar...")
    return region

def Consecuencias():
    global region_actual, ultimo_epicentro, ultimo_grado, ultimo_afectadas
    
    if region_actual is None:
        print("Primero debe cargar una región")
        input("Presiona Enter para continuar...")
        return
    
    print("\n" + "="*50)
    print("ESTIMACIÓN DE CONSECUENCIAS DE TERREMOTO")
    print("="*50)
    
    try:
        M = region_actual['M']
        N = region_actual['N']
        
        print(f"\nDimensiones de la región: {M}x{N}")
        i = int(input(f"Fila del epicentro (1 a {M}): "))
        j = int(input(f"Columna del epicentro (1 a {N}): "))
        g = int(input("Intensidad del terremoto (1-7): "))
        
        if not (1 <= i <= M) or not (1 <= j <= N):
            print("Epicentro fuera de rango")
            input("Presiona Enter para continuar...")
            return
        
        if not (1 <= g <= 7):
            print("Intensidad debe estar entre 1 y 7")
            input("Presiona Enter para continuar...")
            return
        
        # Convertir a 0-based
        i_idx = i - 1
        j_idx = j - 1
        
        # Calcular impacto
        costo_total, fallecidos_total, matriz_afectados = calcular_impacto(
            region_actual, i_idx, j_idx, g
        )
        
        # Guardar para mostrar después
        ultimo_epicentro = (i, j)
        ultimo_grado = g
        ultimo_afectadas = matriz_afectados
        
        # Mostrar resultados
        print("\n" + "="*60)
        print(Fore.YELLOW + "RESULTADOS DE LA ESTIMACIÓN" + Style.RESET_ALL)
        print("="*60)
        print(f"Epicentro: [{i},{j}]")
        print(f"Intensidad: {g}")
        print(f"Celdas afectadas: {np.sum(matriz_afectados)} de {M*N}")
        print("-" * 60)
        print(Fore.CYAN + f"PÉRDIDAS ECONÓMICAS TOTALES: {costo_total} unidades" + Style.RESET_ALL)
        print(Fore.RED + f"PÉRDIDAS HUMANAS TOTALES: {fallecidos_total} personas" + Style.RESET_ALL)
        print(Fore.YELLOW + f"IMPACTO TOTAL (costo + vidas): {costo_total + fallecidos_total}" + Style.RESET_ALL)
        print("="*60)
        
        # Preguntar si quiere ver la región con afectados
        ver = input("\n¿Ver región con áreas afectadas? (s/n): ").lower()
        if ver == 's':
            mostrar_region_completa(
                region_actual, 
                epicentro=(i, j),
                grado=g,
                matriz_afectados=matriz_afectados
            )
            
    except ValueError:
        print("Error: Ingrese valores numéricos válidos")
    
    input("\nPresiona Enter para continuar...")

def ZonaRiesgo():
    global region_actual
    
    if region_actual is None:
        print("Primero debe cargar una región")
        input("Presiona Enter para continuar...")
        return
    
    print("\n" + "="*50)
    print("ZONAS DE MÁXIMO Y MÍNIMO RIESGO")
    print("="*50)
    
    try:
        g = int(input("Intensidad del terremoto (1-7): "))
        
        if not (1 <= g <= 7):
            print("Intensidad debe estar entre 1 y 7")
            input("Presiona Enter para continuar...")
            return
        
        print("\nCalculando...")
        
        # Buscar zonas de riesgo
        pos_mayor, impacto_mayor, pos_menor, impacto_menor = buscar_zonas_riesgo(
            region_actual, g
        )
        
        if pos_mayor is None:
            print("Error en el cálculo")
            input("Presiona Enter para continuar...")
            return
        
        # Mostrar resultados
        print("\n" + "="*60)
        print(Fore.YELLOW + "RESULTADOS DE ANÁLISIS DE RIESGO" + Style.RESET_ALL)
        print("="*60)
        print(f"Intensidad analizada: {g}")
        print("-" * 60)
        print(Fore.RED + "ZONA DE MÁXIMO RIESGO:" + Style.RESET_ALL)
        print(f"  Epicentro: [{pos_mayor[0]},{pos_mayor[1]}]")
        print(f"  Impacto total estimado: {impacto_mayor}")
        print("-" * 60)
        print(Fore.GREEN + "ZONA DE MÍNIMO RIESGO:" + Style.RESET_ALL)
        print(f"  Epicentro: [{pos_menor[0]},{pos_menor[1]}]")
        print(f"  Impacto total estimado: {impacto_menor}")
        print("="*60)
        
        # Mostrar región con ambos epicentros marcados
        print("\n" + Fore.CYAN + "VISUALIZACIÓN EN LA REGIÓN:" + Style.RESET_ALL)
        
        # Crear matriz especial para mostrar
        M = region_actual['M']
        N = region_actual['N']
        
        print("\nLeyenda: ⭐ = Máximo riesgo  ⭕ = Mínimo riesgo")
        for i in range(M):
            for j in range(N):
                pos_actual = (i+1, j+1)
                if pos_actual == pos_mayor:
                    print(Fore.RED + "⭐" + Style.RESET_ALL, end=" ")
                elif pos_actual == pos_menor:
                    print(Fore.GREEN + "⭕" + Style.RESET_ALL, end=" ")
                else:
                    costo = region_actual['costo'][i, j]
                    if costo < 30:
                        print("🟩", end=" ")
                    elif costo < 60:
                        print("🟨", end=" ")
                    else:
                        print("🟥", end=" ")
            print()
            
    except ValueError:
        print("Error: Ingrese un valor numérico válido")
    
    input("\nPresiona Enter para continuar...")

# ========== PROGRAMA PRINCIPAL ==========

def main():
    global region_actual, ultimo_epicentro, ultimo_grado, ultimo_afectadas
    
    # Programa Principal
    print(Fore.BLUE + "="*60)
    print("PROYECTO TERREMOTO - CERT")
    print("UNIVERSIDAD CATÓLICA ANDRÉS BELLO")
    print("FACULTAD DE INGENIERÍA - INFORMÁTICA")
    print("="*60 + Style.RESET_ALL)
    print(Fore.YELLOW + "Elaborado por: Adrian Garcia, Nelson Villaroel y Gabriel Chiquito")
    print(Style.RESET_ALL)
    
    while True:
        print("\n" + "="*60)
        print(Fore.CYAN + "MENÚ PRINCIPAL - SISTEMA CERT" + Style.RESET_ALL)
        print("="*60)
        print("1. Carga o Modificación de costos económicos y pérdidas humanas")
        print("2. Estimación de las consecuencias de un terremoto")
        print("3. Estimación de la zona de máximo y mínimo riesgo")
        print("4. Mostrar la región geográfica")
        print("5. Salir del programa")
        print("-" * 60)
        
        try:
            opcion = int(input("Seleccione una opción (1-5): "))
        except ValueError:
            print(Fore.RED + "Error: Ingrese un número válido" + Style.RESET_ALL)
            continue
        
        if opcion == 1: 
            print("\n" + "="*50)
            print(Fore.CYAN + "CARGA O MODIFICACIÓN DE DATOS" + Style.RESET_ALL)
            print("="*50)
            print("1. Cargar región desde archivo ENTRA.TXT")
            print("2. Crear región manualmente (datos aleatorios)")
            print("3. Modificar celda individual")
            print("4. Volver al menú principal")
            
            try:
                subopcion = int(input("\nElija subopción (1-4): "))
            except ValueError:
                print("Opción inválida")
                continue
                
            if subopcion == 1:
                region_actual = cargar_archivo()
            elif subopcion == 2: 
                region_actual = entrada_manual()
            elif subopcion == 3:
                region_actual = Modificar(region_actual)
            elif subopcion == 4: 
                print("Volviendo al menú principal...")
            else:
                print("Opción no válida")
                
        elif opcion == 2: 
            Consecuencias()
            
        elif opcion == 3:
            ZonaRiesgo()
            
        elif opcion == 4:
            if region_actual is None:
                print(Fore.RED + "\n✗ No hay región cargada" + Style.RESET_ALL)
                print("Use la opción 1 para cargar o crear una región")
                input("Presiona Enter para continuar...")
            else:
                # Mostrar con o sin epicentro
                if ultimo_epicentro is not None and ultimo_afectadas is not None:
                    mostrar_region_completa(
                        region_actual,
                        epicentro=ultimo_epicentro,
                        grado=ultimo_grado,
                        matriz_afectadas=ultimo_afectadas
                    )
                else:
                    mostrar_region_completa(region_actual)
                input("\nPresiona Enter para continuar...")
                
        elif opcion == 5:
            print("\n" + "="*60)
            print(Fore.GREEN + "¡Gracias por utilizar el Sistema CERT!")
            print("Desarrollado para la Comisión de Estimación de Riesgos en Terremotos")
            print("UCAB - Semestre Sep-Ene 2026" + Style.RESET_ALL)
            print("="*60)
            break
            
        else:
            print(Fore.RED + "Opción no válida. Intente de nuevo." + Style.RESET_ALL)
main()