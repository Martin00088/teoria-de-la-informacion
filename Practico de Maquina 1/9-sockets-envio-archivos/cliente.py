import socket
import zlib


def comprimir_mensaje(mensaje, alfabeto):
    # Comprimir usando el alfabeto proporcionado
    comprimido = []
    for char in mensaje:
        if char in alfabeto:
            comprimido.append(str(alfabeto.index(char)))
        else:
            comprimido.append(char)
    return ",".join(comprimido)


def main():
    # Configuración del cliente
    servidor = "127.0.0.1"
    puerto = 5555
    alfabeto = "ABCDEFGH"  # Alfabeto para compresión

    try:
        # Crear socket y conectar
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((servidor, puerto))
        print("[*] Conectado al servidor")

        # Leer archivo a enviar
        with open("archivo_a_enviar.txt", "r") as f:
            contenido = f.read()

        # Comprimir contenido
        contenido_comprimido = comprimir_mensaje(contenido, alfabeto)
        print(f"[*] Contenido comprimido: {contenido_comprimido}")

        # Enviar datos comprimidos
        cliente.send(contenido_comprimido.encode("utf-8"))
        print("[*] Archivo comprimido enviado")

        # Recibir confirmación
        respuesta = cliente.recv(4096)
        print(f"[*] Respuesta del servidor: {respuesta.decode('utf-8')}")

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        cliente.close()


if __name__ == "__main__":
    main()
