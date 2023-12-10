import subprocess
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

def check_connection(ip, port=8333):
    try:
        # Intenta conectar usando nc o telnet dependiendo del sistema operativo
        if platform.system() == "Windows":
            subprocess.run(["telnet", ip, str(port)], check=True)
        else:
            subprocess.run(["nc", "-zv", ip, str(port)], check=True)

        print(f"Conexión exitosa a {ip} en el puerto {port}")
    except subprocess.CalledProcessError as e:
        print(f"Fallo al conectar a {ip} en el puerto {port}: {e}")
        sys.exit(1)

# Abrir el puerto 8333 en el firewall
open_firewall_port()

# Reemplaza 'x.x.x.x' con la IP del objetivo
# check_connection("x.x.x.x")
