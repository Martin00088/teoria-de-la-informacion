# Sistema de Registro de Personas - Comparación de Formatos

Este proyecto es una aplicación web que permite registrar información de personas y compara el tamaño de almacenamiento entre dos formatos de archivo diferentes: formato de longitud fija y formato de longitud variable (JSON).


##  Formatos de Archivo

### 1. Formato de Longitud Fija (.dat)
- Cada campo tiene una longitud predefinida
- Estructura: `Nombre(30) + Dirección(50) + DNI(10) + Campos(8)`
- Total por registro: 98 caracteres → 98 bytes (ASCII)

### 2. Formato de Longitud Variable (JSON)
- Estructura flexible con etiquetas
- Solo almacena la información necesaria
- Incluye metadatos (nombres de campos)

##  Comparativa de Tamaños

El sistema calcula y muestra:
- El contenido simulado de ambos archivos
- El tamaño en bytes de cada formato
- La diferencia porcentual entre ambos



## Uso

1. Clonar o descargar los archivos del proyecto
2. Abrir el archivo `index.html` en un navegador web
3. Completa el formulario con los datos de la persona
4. Haz clic en "Agregar" para registrar la información
5. Observar los resultados en la sección inferior

