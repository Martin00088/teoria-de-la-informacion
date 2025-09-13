import os
import time
import zstandard as zstd

# Carpeta donde están los archivos
carpeta = "./archivos/"
archivos = [
    "Ejemplo_AVI_1920.avi",
    "Ejemplo_MP3.mp3",
    "Ejemplo_MP4_1920.mp4",
    "Ejemplo_WAV.wav",
    "Los_Tres_Mosqueteros.doc",
]

# Niveles de compresión a probar
niveles = {"rápida": 1, "normal": 11, "lenta": 22}


def benchmark_zstd():
    resultados = []

    for archivo in archivos:
        ruta = os.path.join(carpeta, archivo)
        if not os.path.isfile(ruta):
            print(f"Archivo no encontrado: {ruta}")
            continue

        with open(ruta, "rb") as f:
            data = f.read()

        tamaño_original = len(data)

        for nombre_nivel, nivel in niveles.items():
            cctx = zstd.ZstdCompressor(level=nivel)

            inicio = time.time()
            comprimido = cctx.compress(data)
            fin = time.time()

            tamaño_comprimido = len(comprimido)
            ratio = tamaño_comprimido / tamaño_original
            tiempo = fin - inicio

            resultados.append(
                {
                    "archivo": archivo,
                    "nivel": nombre_nivel,
                    "tamaño_original": tamaño_original,
                    "tamaño_comprimido": tamaño_comprimido,
                    "ratio": ratio,
                    "tiempo": tiempo,
                }
            )

    # Mostrar resultados con mejor formato
    print(
        f"{'Archivo':25} {'Nivel':10} {'Original (MB)':12} {'Comprimido (MB)':15} {'Ratio':8} {'Tiempo (s)':12}"
    )
    print("-" * 85)

    for i, r in enumerate(resultados):
        # Añadir línea separadora entre diferentes archivos
        if i > 0 and r["archivo"] != resultados[i - 1]["archivo"]:
            print("-" * 85)

        print(
            f"{r['archivo']:25} {r['nivel']:10} {r['tamaño_original']/1e6:12.2f} {r['tamaño_comprimido']/1e6:15.2f} {r['ratio']:8.4f} {r['tiempo']:12.6f}"
        )


if __name__ == "__main__":
    benchmark_zstd()
