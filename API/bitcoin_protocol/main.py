import subprocess
import socket
import threading
import platform
import sys


def open_firewall_port(port=8333):
    os_type = platform.system()

    try:
        if os_type == "Linux":
            # Comandos para Linux
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", str(port), "-j", "ACCEPT"], check=True)
            subprocess.run(["sudo", "iptables-save"], check=True)
        elif os_type == "Darwin":
            # Comandos para macOS (No hay una forma estándar de hacer esto en macOS, se asume que el puerto está abierto)
            print("macOS detectado. Asegúrate de que el puerto 8333 esté abierto manualmente.")
        elif os_type == "Windows":
            # Comandos para Windows
            subprocess.run(f"netsh advfirewall firewall add rule name=\"Open Port {port}\" dir=in action=allow protocol=TCP localport={port}", shell=True, check=True)
        else:
            print(f"Sistema operativo no soportado: {os_type}")
            return

        print(f"El puerto {port} ha sido abierto en el firewall para {os_type}.")
    except subprocess.CalledProcessError as e:
        print(f"Error al abrir el puerto {port} en {os_type}: {e}")
        sys.exit(1)

# Abrir el puerto 8333 en el firewall
# open_firewall_port()

# Función para manejar conexiones entrantes
def handle_connection(conn, addr):
    print(f"Conexión entrante de {addr}")
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Mensaje de {addr}: {data.decode()}")
    conn.close()

# Función para iniciar el servidor
def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Escuchando en el puerto {port}...")

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_connection, args=(conn, addr))
        client_thread.start()

# Función para enviar mensajes a otros nodos
def send_message(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(message.encode())
        print("Mensaje enviado.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: script.py [local_port] [remote_ip:remote_port] [message]")
        sys.exit(1)

    local_port = int(sys.argv[1])
    remote_info = sys.argv[2].split(":")
    remote_ip = remote_info[0]
    remote_port = int(remote_info[1])
    message = sys.argv[3]

    # Iniciar el servidor en un hilo separado
    server_thread = threading.Thread(target=start_server, args=(local_port,))
    server_thread.start()

    # Enviar mensaje al nodo remoto
    send_message(remote_ip, remote_port, message)
