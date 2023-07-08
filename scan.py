# Sencillo escaner de red
# Guiado del scan de xerosploit
# Creado por Wuilmer Bolivar
# Fecha: 08/07/2023
# Libre uso y modificación solo mencionar al autor

from terminaltables import DoubleTable
from tabulate import tabulate
import os
import time

def imprimir_configuracion_red():
    n_ip = os.popen("hostname -I").read().strip()  # Obtén la dirección IP local
    n_mac = os.popen("ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'").read().strip()  # Obtén la dirección MAC de la red
    n_host = os.popen("hostname").read().strip()  # Obtén el nombre del host

    print("Configuración de tu red\n")
    table = [
        ["Dirección IP", "Dirección MAC", "Nombre de host"],
        [n_ip, n_mac.upper(), n_host]
    ]
    print(tabulate(table, stralign="center", tablefmt="fancy_grid", headers="firstrow"))
    print()

def escanear_red():
    n_ip = os.popen("hostname -I").read().strip()  # Obtén la dirección IP local

    print("[*] Escaneando la red...")
    time.sleep(1)  # Simula el tiempo de escaneo

    scan = os.popen("nmap -O -p 1-1000 " + n_ip + "/24 -n").read()

    with open('escaneo.txt', 'w') as f:
        f.write(scan)

    dispositivos = os.popen("grep report escaneo.txt | awk '{print $5}'").read()

    dispositivos_mac = os.popen(
        "grep MAC escaneo.txt | awk '{print $3}'").read() + os.popen(
        "ip addr | grep 'state UP' -A1 | tail -n1 | awk '{print $2}' | cut -f1  -d'/'").read().upper()

    dispositivos_nombre = os.popen(
        "grep MAC escaneo.txt | awk '{print $4 ,S$5 $6}'").read() + "\033[1;32m(Este dispositivo)\033[1;m"

    table_data = [
        ['Dirección IP', 'Dirección MAC', 'Fabricante'],
        [dispositivos, dispositivos_mac, dispositivos_nombre]
    ]
    table = DoubleTable(table_data)
    print("[+]═════════════[ Dispositivos encontrados en tu red ]═════════════[+]\n")
    print(table.table)

imprimir_configuracion_red()
escanear_red()
