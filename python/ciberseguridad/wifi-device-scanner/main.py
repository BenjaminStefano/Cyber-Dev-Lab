from __future__ import annotations

import argparse
import ipaddress
import socket
import sys
import time
from datetime import datetime
from typing import TypedDict

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from scapy.all import ARP, Ether, srp


APP_NAME = "WiFi Device Scanner"
APP_VERSION = "1.0.0"
MAX_NETWORK_ADDRESSES = 1024

console = Console()


class Device(TypedDict):
    ip: str
    mac: str
    hostname: str
    role: str


def validate_network(value: str) -> str:
    """Valida y normaliza una red IPv4 escrita en formato CIDR."""
    try:
        network = ipaddress.ip_network(value, strict=False)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "La red no es válida. Ejemplo correcto: 192.168.1.0/24"
        ) from error

    if network.version != 4:
        raise argparse.ArgumentTypeError(
            "Esta versión solamente admite redes IPv4."
        )

    if network.num_addresses > MAX_NETWORK_ADDRESSES:
        raise argparse.ArgumentTypeError(
            f"El rango máximo permitido es de "
            f"{MAX_NETWORK_ADDRESSES} direcciones."
        )

    return str(network)


def validate_timeout(value: str) -> int:
    """Valida el tiempo de espera del escaneo."""
    try:
        timeout = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "El timeout debe ser un número entero."
        ) from error

    if not 1 <= timeout <= 10:
        raise argparse.ArgumentTypeError(
            "El timeout debe estar entre 1 y 10 segundos."
        )

    return timeout


def get_local_ip() -> str:
    """
    Obtiene la dirección IPv4 utilizada por el equipo en la red.

    No envía información de aplicación. El socket se utiliza para que
    el sistema operativo seleccione la interfaz de salida apropiada.
    """
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        connection.connect(("8.8.8.8", 80))
        return connection.getsockname()[0]
    except OSError:
        return "No disponible"
    finally:
        connection.close()


def resolve_hostname(ip_address: str) -> str:
    """Intenta resolver el nombre de host de una dirección IP."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except (socket.herror, socket.gaierror, TimeoutError, OSError):
        return "No disponible"


def determine_role(ip_address: str, local_ip: str) -> str:
    """Asigna un rol básico al dispositivo encontrado."""
    if ip_address == local_ip:
        return "Este equipo"

    return "Dispositivo"


def scan_network(
    network: str,
    local_ip: str,
    timeout: int,
) -> list[Device]:
    """Descubre dispositivos activos mediante solicitudes ARP."""
    arp_request = ARP(pdst=network)
    broadcast_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast_frame / arp_request

    answered_packets, _ = srp(
        packet,
        timeout=timeout,
        verbose=False,
    )

    devices_by_mac: dict[str, Device] = {}

    for _, response in answered_packets:
        ip_address = str(response.psrc)
        mac_address = str(response.hwsrc).upper()

        devices_by_mac[mac_address] = {
            "ip": ip_address,
            "mac": mac_address,
            "hostname": resolve_hostname(ip_address),
            "role": determine_role(ip_address, local_ip),
        }

    return sorted(
        devices_by_mac.values(),
        key=lambda device: ipaddress.ip_address(device["ip"]),
    )


def create_banner() -> Panel:
    """Construye el banner principal."""
    title = Text()
    title.append("WiFi ", style="bold cyan")
    title.append("Device Scanner", style="bold bright_blue")
    title.append(f"\nVersion {APP_VERSION}", style="dim")

    return Panel(
        title,
        subtitle="Network discovery tool",
        border_style="bright_blue",
        box=box.DOUBLE,
        expand=False,
        padding=(1, 5),
    )


def create_scan_information(
    network: str,
    local_ip: str,
    timeout: int,
) -> Panel:
    """Construye el panel con la configuración del escaneo."""
    information = Table.grid(padding=(0, 2))
    information.add_column(style="bold cyan", justify="right")
    information.add_column(style="white")

    information.add_row("Red objetivo", network)
    information.add_row("IP local", local_ip)
    information.add_row("Timeout", f"{timeout} segundos")
    information.add_row(
        "Inicio",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    return Panel(
        information,
        title="[bold]Configuración del escaneo[/bold]",
        border_style="cyan",
        box=box.ROUNDED,
    )


def create_devices_table(devices: list[Device]) -> Table:
    """Construye la tabla de dispositivos descubiertos."""
    table = Table(
        title="Dispositivos detectados",
        title_style="bold bright_blue",
        header_style="bold white on blue",
        border_style="bright_blue",
        box=box.ROUNDED,
        show_lines=True,
        expand=True,
    )

    table.add_column("#", justify="right", style="dim", width=4)
    table.add_column("Dirección IP", style="cyan", no_wrap=True)
    table.add_column("Dirección MAC", style="magenta", no_wrap=True)
    table.add_column("Hostname", style="white")
    table.add_column("Rol", justify="center")

    for index, device in enumerate(devices, start=1):
        role = device["role"]

        if role == "Este equipo":
            formatted_role = "[bold green]Este equipo[/bold green]"
        else:
            formatted_role = "[yellow]Dispositivo[/yellow]"

        table.add_row(
            str(index),
            device["ip"],
            device["mac"],
            device["hostname"],
            formatted_role,
        )

    return table


def print_summary(
    devices: list[Device],
    network: str,
    duration: float,
) -> None:
    """Muestra el resumen final del escaneo."""
    summary = Table.grid(padding=(0, 2))
    summary.add_column(style="bold cyan", justify="right")
    summary.add_column(style="white")

    summary.add_row("Estado", "[bold green]Completado[/bold green]")
    summary.add_row("Red analizada", network)
    summary.add_row("Dispositivos", str(len(devices)))
    summary.add_row("Duración", f"{duration:.2f} segundos")
    summary.add_row(
        "Finalización",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    console.print(
        Panel(
            summary,
            title="[bold green]Resumen del escaneo[/bold green]",
            border_style="green",
            box=box.ROUNDED,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    """Configura los argumentos de la línea de comandos."""
    parser = argparse.ArgumentParser(
        prog="wifi-device-scanner",
        description=(
            "Descubre dispositivos conectados a una red local "
            "mediante solicitudes ARP."
        ),
        epilog=(
            "Utiliza esta herramienta únicamente en redes propias "
            "o donde tengas autorización explícita."
        ),
    )

    parser.add_argument(
        "network",
        type=validate_network,
        help="Red IPv4 en formato CIDR. Ejemplo: 192.168.1.0/24",
    )

    parser.add_argument(
        "-t",
        "--timeout",
        type=validate_timeout,
        default=2,
        metavar="SEGUNDOS",
        help="Tiempo de espera entre 1 y 10 segundos. Valor inicial: 2",
    )

    return parser


def main() -> None:
    """Punto de entrada principal de la aplicación."""
    parser = build_parser()
    arguments = parser.parse_args()

    local_ip = get_local_ip()

    console.print()
    console.print(create_banner())
    console.print()

    console.print(
        "[yellow]Aviso:[/yellow] utiliza esta herramienta únicamente "
        "en redes propias o autorizadas.\n"
    )

    console.print(
        create_scan_information(
            network=arguments.network,
            local_ip=local_ip,
            timeout=arguments.timeout,
        )
    )

    start_time = time.perf_counter()

    try:
        with console.status(
            "[bold cyan]Escaneando la red y resolviendo dispositivos...",
            spinner="dots",
            spinner_style="bright_blue",
        ):
            devices = scan_network(
                network=arguments.network,
                local_ip=local_ip,
                timeout=arguments.timeout,
            )

    except PermissionError:
        console.print(
            Panel(
                "Ejecuta PowerShell como administrador o utiliza "
                "[bold]sudo[/bold] en Linux.",
                title="[bold red]Permisos insuficientes[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)

    except RuntimeError as error:
        console.print(
            Panel(
                str(error),
                title="[bold red]Error de captura de red[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)

    except OSError as error:
        console.print(
            Panel(
                str(error),
                title="[bold red]Error de red[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)

    except KeyboardInterrupt:
        console.print(
            "\n[yellow]Escaneo cancelado por el usuario.[/yellow]"
        )
        sys.exit(130)

    duration = time.perf_counter() - start_time

    console.print()

    if devices:
        console.print(create_devices_table(devices))
    else:
        console.print(
            Panel(
                "No se encontraron dispositivos activos.\n\n"
                "Comprueba el rango de red, los permisos y la conexión.",
                title="[bold yellow]Sin resultados[/bold yellow]",
                border_style="yellow",
            )
        )

    console.print()
    print_summary(
        devices=devices,
        network=arguments.network,
        duration=duration,
    )

    console.print(
        "\n[dim]WiFi Device Scanner "
        f"v{APP_VERSION} · Cyber-Dev-Lab[/dim]\n"
    )


if __name__ == "__main__":
    main()