import socket
import threading
import time
import sys

# funcion para conectar con reintentos automaticos
def conectar_al_servidor(server_ip="127.0.0.1", server_port=8000):
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((server_ip, server_port))
            print(f"Conectado a {server_ip}:{server_port}")
            return client
        except (ConnectionRefusedError, OSError):
            print("Servidor no disponible. Reintentando en 3 segundos...")
            time.sleep(3)

# funcion para recibir mensajes
def recibir_mensajes(client):
    while True:
        try:
            response = client.recv(1024)
            if not response:
                print("\n[Servidor desconectado] Presiona ENTER para reconectar...")
                # Cerramos el socket para que el hilo principal detecte el error al intentar enviar
                client.close() 
                break
            print(f"\n{response.decode('utf-8')}")
            print("Escribe tu mensaje: ", end="", flush=True)
        except OSError:
            break

def run_client():
    server_ip = "127.0.0.1"
    server_port = 8000
    name = None

    while True: # bucle principal de reconexion
        client = conectar_al_servidor(server_ip, server_port)

        if name is None:
            try:
                # recibir mensaje de bienvenida del servidor primero
                print(client.recv(1024).decode("utf-8")) 
                name = input(">  ")
            except OSError:
                continue # si falla al inicio, reintenta conectar
        else:
            print(f"Bienvenido de nuevo, {name}")
            print("Escribe tu mensaje: ", end="", flush=True)

        # enviamos el nombre para identificarnos ante el servidor
        try:
            client.send(name.encode("utf-8"))
        except OSError:
            continue

        # iniciamos el hilo de escucha (daemon = se cierra si el programa principal se cierra)
        hilo_escucha = threading.Thread(target=recibir_mensajes, args=(client,), daemon=True)
        hilo_escucha.start()

        # bucle de envio (Hilo Principal)
        while True:
            try:
                msg = input() # bloquea el hilo principal esperando al usuario
                
                if msg.lower() == "close":
                    client.close()
                    sys.exit() # Cierra el programa completamente

                client.send(msg.encode("utf-8"))
            
            except (BrokenPipeError, OSError):
                print("\nConexión perdida. Intentando recuperar sesión...")
                client.close()
                break # rompe este bucle para volver al while principal y reconectar

if __name__ == "__main__":
    try:
        run_client()
    except KeyboardInterrupt:
        print("\nSaliendo...")