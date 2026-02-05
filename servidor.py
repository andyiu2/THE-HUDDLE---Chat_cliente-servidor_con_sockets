import socket
import threading
import time
clients = {} # diccionario para manejar los clientes activos

def broadcast(message, emisor): 
    """Envía un mensaje a todos los clientes menos al remitente"""
    for client in list(clients.keys()):
        if client != emisor:
            try:
                client.send(message.encode("utf-8"))
            except:
                client.close()
                del clients[client]

def manejar_cliente(client_socket, addr):
    try:
        client_socket.send("Ingrese su nombre: ".encode("utf-8"))
        name = client_socket.recv(1024).decode("utf-8").strip()
        if not name:
            name = f"Usuari0_{addr[1]}"
        clients[client_socket] = name

        print(f"{name} ({addr[0]}:{addr[1]}) se ha conectado")
        broadcast(f"{name} se unio al chat", client_socket)

        while True:
            request = client_socket.recv(1024).decode("utf-8")
            if not request:
                break  # el cliente se desconectó
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break

            print(f"{name} dice: {request}")
            broadcast(f"{name}: {request}", client_socket)


    except Exception as e:
        print(f"Error manejando cliente {addr}: {e}")
    finally:
        if client_socket in clients:
            del clients[client_socket]
        client_socket.close()
        print(f"Conexión cerrada con {name}")
        broadcast(f"{name} se ha desconectado del chat", client_socket)

def iniciar_servidor():
    server_ip = "127.0.0.1"
    port = 8000

    while True:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creamos el socket del servidor
            server.bind((server_ip, port)) # asinga una direccion IP y puerto especifico al socket del servidor
            server.listen() # ponemos al socket en modo servidor, empieza a esperar conexiones
            print(f"Servidor escuchando en {server_ip}:{port}")

            while True:
                try:
                    client_socket, addr = server.accept() # acepta una conexion entrante y devuelve un nuevo socket para hablar con ese cliente (accept es un metodo bloqueante) 
                    # un hilo es un "subprograma" que se ejecuta en paralelo dentro del mismo proceso 
                    thread = threading.Thread(target=manejar_cliente, args=(client_socket, addr), daemon=True) # creamos un hilo para manejar al cliente que se conecte
                    thread.start() # llama internamente a la funcion que colocamos en el target 
                    print(f"Conexión aceptada de {addr[0]}:{addr[1]}")

                except Exception as e:
                    print(f"Error aceptando conexion: {e}")
                    time.sleep(1)
                    
        except OSError as e:
            print(f"Error de socket: {e}")
            print("Reintentando iniciar el servidor en 3 segundos...")
            time.sleep(3)

        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario")
            break
            
        finally: # siempre se ejecuta 
            try:
                server.close()
                print("Servidor cerrado.")
            except:
                pass

iniciar_servidor()
