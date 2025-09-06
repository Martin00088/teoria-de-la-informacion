import socket
import zlib


def descomprimir_mensaje(mensaje_comprimido, alfabeto):
    # Descomprimir usando el alfabeto proporcionado
    datos_descomprimidos_zlib = zlib.decompress(mensaje_comprimido).decode("utf-8")

    partes = datos_descomprimidos_zlib.split(",")
    descomprimido = []
    for parte in partes:
        if parte.isdigit() and int(parte) < len(alfabeto):
            descomprimido.append(alfabeto[int(parte)])
        else:
            descomprimido.append(parte)

    return "".join(descomprimido)


def manejar_cliente(socket_cliente):
    alfabeto = "ABCDEFGH"

    try:

        datos = socket_cliente.recv(4096)
        print(f"[*] Datos comprimidos recibidos: {datos}")
        print(f"[*] Tamaño de datos recibidos: {len(datos)} bytes")

        # Descomprimir datos
        datos_descomprimidos = descomprimir_mensaje(datos, alfabeto)
        print(f"[*] Datos descomprimidos: {datos_descomprimidos}")

        # Guardar en archivo
        with open("archivo_recibido.txt", "w") as f:
            f.write(datos_descomprimidos)

        # Enviar confirmación
        socket_cliente.send(
            "Archivo recibido y descomprimido correctamente".encode("utf-8")
        )

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        socket_cliente.close()


def main():
    host = "127.0.0.1"
    puerto = 5555

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, puerto))
    servidor.listen(1)
    print(f"[*] Servidor escuchando en {host}:{puerto}")

    try:
        while True:
            cliente, direccion = servidor.accept()
            print(f"[*] Conexión aceptada de {direccion[0]}:{direccion[1]}")
            manejar_cliente(cliente)
    except KeyboardInterrupt:
        print("\n[*] Cerrando servidor...")
    finally:
        servidor.close()


if __name__ == "__main__":
    main()
