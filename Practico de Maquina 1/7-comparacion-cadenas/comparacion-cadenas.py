def distancia_levenshtein(cadena1, cadena2):
    """
    Calcula la distancia de Levenshtein entre dos cadenas.
    Esta distancia representa el número mínimo de operaciones (inserción, eliminación o sustitución)
    necesarias para convertir una cadena en la otra.
    """
    # Crear una matriz de tamaño (len(cadena1)+1) x (len(cadena2)+1)
    m = len(cadena1)
    n = len(cadena2)
    matriz = [[0] * (n + 1) for _ in range(m + 1)]
   
    # Inicializar la primera columna
    for i in range(m + 1):
        matriz[i][0] = i
   
    # Inicializar la primera fila
    for j in range(n + 1):
        matriz[0][j] = j
   
    # Llenar la matriz
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if cadena1[i - 1] == cadena2[j - 1]:
                costo = 0
            else:
                costo = 1
           
            matriz[i][j] = min(
                matriz[i - 1][j] + 1,      # Eliminación
                matriz[i][j - 1] + 1,      # Inserción
                matriz[i - 1][j - 1] + costo  # Sustitución
            )
   
    return matriz[m][n]


def porcentaje_similitud(cadena1, cadena2):
    """
    Calcula el porcentaje de similitud entre dos cadenas basado en la distancia de Levenshtein.
    """
    distancia = distancia_levenshtein(cadena1, cadena2)
    longitud_maxima = max(len(cadena1), len(cadena2))
   
    if longitud_maxima == 0:
        return 100.0  # Ambas cadenas están vacías
   
    similitud = (1 - distancia / longitud_maxima) * 100
    return round(similitud, 2)


def comparar_cadenas(cadena1, cadena2, umbral=70.0):
    """
    Compara dos cadenas y muestra información detallada sobre su similitud.
    """
    distancia = distancia_levenshtein(cadena1, cadena2)
    similitud = porcentaje_similitud(cadena1, cadena2)
   
    print(f"Cadena 1: '{cadena1}'")
    print(f"Cadena 2: '{cadena2}'")
    print(f"Distancia de Levenshtein: {distancia}")
    print(f"Porcentaje de similitud: {similitud}%")
   
    if similitud >= umbral:
        print(f"Resultado: Las cadenas son muy parecidas (≥ {umbral}% de similitud)")
    else:
        print(f"Resultado: Las cadenas son diferentes (< {umbral}% de similitud)")
   
    print("-" * 50)
    return similitud


# Ejemplos de uso con los casos propuestos
if __name__ == "__main__":
    print("COMPARADOR DE CADENAS CON ALGORITMO DE LEVENSHTEIN")
    print("=" * 50)
   
    # Caso 1: Juan Perez vs Jaun Perez
    comparar_cadenas("Juan Perez", "Jaun Perez")
   
    # Caso 2: Horacio Lopez vs Oracio Lopez
    comparar_cadenas("Horacio Lopez", "Oracio Lopez")
   
    # Casos adicionales para demostración
    comparar_cadenas("Hola mundo", "Hola mundo")  # Idénticas
    comparar_cadenas("gato", "gato")              # Idénticas
    comparar_cadenas("gato", "gatito")            # Similares
    comparar_cadenas("python", "java")            # Diferentes
   
    # Ejemplo interactivo
    print("PRUEBA INTERACTIVA")
    print("=" * 30)
   
    while True:
        try:
            cad1 = input("Ingrese la primera cadena (o 'salir' para terminar): ")
            if cad1.lower() == 'salir':
                break
           
            cad2 = input("Ingrese la segunda cadena: ")
           
            comparar_cadenas(cad1, cad2)
           
        except KeyboardInterrupt:
            print("\nPrograma terminado.")
            break
        except Exception as e:
            print(f"Error: {e}")

