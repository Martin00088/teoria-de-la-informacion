import math
from collections import Counter
import os
import sys


def calcular_entropia(frecuencias, total):
    """Calcula la entropía de orden cero a partir de frecuencias"""
    entropia = 0.0
    for freq in frecuencias.values():
        if freq > 0:
            p = freq / total
            entropia -= p * math.log2(p)
    return entropia


def calcular_entropia_orden1(bigramas, total_bigramas):
    """Calcula la entropía de primer orden (bigramas)"""
    entropia = 0.0
    for freq in bigramas.values():
        if freq > 0:
            p = freq / total_bigramas
            entropia -= p * math.log2(p)
    return entropia


def calcular_redundancia(entropia, max_entropia):
    """Calcula la redundancia de la fuente"""
    if max_entropia == 0:
        return 0
    return 1 - (entropia / max_entropia)


def analizar_fuente(datos, nombre_fuente="texto"):
    """Analiza completamente una fuente de datos"""
    # Estadísticas de caracteres individuales (orden cero)
    total_caracteres = len(datos)
    frecuencias = Counter(datos)
    entropia_orden0 = calcular_entropia(frecuencias, total_caracteres)
   
    # Calcular máxima entropía posible (todos los símbolos equiprobables)
    simbolos_unicos = len(frecuencias)
    max_entropia_orden0 = math.log2(simbolos_unicos) if simbolos_unicos > 0 else 0
    redundancia_orden0 = calcular_redundancia(entropia_orden0, max_entropia_orden0)
   
    # Estadísticas de bigramas (primer orden)
    if total_caracteres > 1:
        total_bigramas = total_caracteres - 1
        bigramas = Counter([datos[i:i+2] for i in range(total_bigramas)])
        entropia_orden1 = calcular_entropia_orden1(bigramas, total_bigramas)
       
        # Para bigramas, la máxima entropía sería log2(N²) donde N es el número de símbolos únicos
        max_entropia_orden1 = math.log2(simbolos_unicos * simbolos_unicos) if simbolos_unicos > 0 else 0
        redundancia_orden1 = calcular_redundancia(entropia_orden1, max_entropia_orden1)
    else:
        entropia_orden1 = 0
        redundancia_orden1 = 0
        bigramas = Counter()
   
    # Presentar resultados
    print(f"\n{'='*60}")
    print(f"ANÁLISIS DE: {nombre_fuente}")
    print(f"{'='*60}")
    print(f"Tamaño: {total_caracteres} bytes")
    print(f"Símbolos únicos: {simbolos_unicos}")
   
    print(f"\nENTROPÍA DE ORDEN CERO (símbolos independientes):")
    print(f"  Entropía: {entropia_orden0:.4f} bits/símbolo")
    print(f"  Máxima entropía posible: {max_entropia_orden0:.4f} bits/símbolo")
    print(f"  Redundancia: {redundancia_orden0:.4f} ({redundancia_orden0*100:.2f}%)")
   
    if total_caracteres > 1:
        print(f"\nENTROPÍA DE PRIMER ORDEN (bigramas dependientes):")
        print(f"  Entropía: {entropia_orden1:.4f} bits/símbolo")
        print(f"  Máxima entropía posible: {max_entropia_orden1:.4f} bits/símbolo")
        print(f"  Redundancia: {redundancia_orden1:.4f} ({redundancia_orden1*100:.2f}%)")
   
    # Mostrar los 5 símbolos más frecuentes
    print(f"\n5 SÍMBOLOS MÁS FRECUENTES:")
    for simbolo, freq in frecuencias.most_common(5):
        if 32 <= simbolo <= 126:  # Caracteres imprimibles
            repr_simbolo = f"'{chr(simbolo)}'"
        else:
            repr_simbolo = f"0x{simbolo:02x}"
        prob = freq / total_caracteres
        print(f"  {repr_simbolo}: {freq} ocurrencias, probabilidad: {prob:.4f}")
   
    return {
        'entropia_orden0': entropia_orden0,
        'redundancia_orden0': redundancia_orden0,
        'entropia_orden1': entropia_orden1,
        'redundancia_orden1': redundancia_orden1,
        'simbolos_unicos': simbolos_unicos
    }


def analizar_archivo(ruta_archivo):
    """Analiza un archivo y muestra sus estadísticas de información"""
    try:
        with open(ruta_archivo, "rb") as f:
            datos = f.read()
       
        nombre = os.path.basename(ruta_archivo)
        return analizar_fuente(datos, nombre)
       
    except Exception as e:
        print(f"Error al procesar el archivo {ruta_archivo}: {e}")
        return None


def analizar_texto(texto):
    """Analiza un texto ingresado directamente"""
    # Convertir el texto a bytes para consistencia con el análisis de archivos
    datos = texto.encode('utf-8')
    return analizar_fuente(datos, "Texto ingresado")


def comparar_archivos(resultados):
    """Compara los resultados de múltiples archivos"""
    if len(resultados) < 2:
        return
   
    print(f"\n{'='*60}")
    print("COMPARACIÓN ENTRE ARCHIVOS")
    print(f"{'='*60}")
   
    # Encabezado de la tabla
    print(f"{'Archivo':<20} {'Símbolos':<10} {'Entropía0':<10} {'Redund0':<10} {'Entropía1':<10} {'Redund1':<10}")
    print("-" * 80)
   
    # Datos de cada archivo
    for nombre, datos in resultados.items():
        print(f"{nombre:<20} {datos['simbolos_unicos']:<10} {datos['entropia_orden0']:<10.4f} "
              f"{datos['redundancia_orden0']:<10.4f} {datos['entropia_orden1']:<10.4f} "
              f"{datos['redundancia_orden1']:<10.4f}")


if __name__ == "__main__":
    resultados = {}
   
    if len(sys.argv) > 1:
        # Modo de línea de comandos: analizar archivos especificados
        for ruta in sys.argv[1:]:
            if os.path.isfile(ruta):
                res = analizar_archivo(ruta)
                if res:
                    resultados[os.path.basename(ruta)] = res
            else:
                print(f"Advertencia: {ruta} no es un archivo válido")
       
        # Mostrar comparación si se analizaron múltiples archivos
        if len(resultados) > 1:
            comparar_archivos(resultados)
    else:
        # Modo interactivo
        while True:
            print("\nOpciones:")
            print("1. Analizar archivo")
            print("2. Ingresar texto manualmente")
            print("3. Salir")
           
            opcion = input("Seleccione una opción: ").strip()
           
            if opcion == "1":
                ruta = input("Ingrese la ruta del archivo: ").strip()
                if os.path.isfile(ruta):
                    res = analizar_archivo(ruta)
                    if res:
                        resultados[os.path.basename(ruta)] = res
                else:
                    print("El archivo no existe o la ruta es incorrecta")
           
            elif opcion == "2":
                texto = input("Ingrese el texto a analizar: ")
                if texto:
                    res = analizar_texto(texto)
                    resultados["Texto ingresado"] = res
           
            elif opcion == "3":
                # Mostrar comparación final si hay múltiples análisis
                if len(resultados) > 1:
                    comparar_archivos(resultados)
                print("Programa finalizado.")
                break
           
            else:
                print("Opción no válida")
