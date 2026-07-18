from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from monitor.baseline import (
    build_baseline,
    load_baseline,
    save_baseline,
)
from monitor.reporting import (
    compare_baselines,
    print_banner,
    print_baseline_created,
    print_scan_results,
)


APP_VERSION = "1.0.0"
DEFAULT_BASELINE_NAME = "baseline.json"

console = Console()


def validate_directory(value: str) -> Path:
    """Valida que el argumento corresponda a un directorio existente."""
    directory = Path(value).expanduser().resolve()

    if not directory.exists():
        raise argparse.ArgumentTypeError(
            f"El directorio no existe: {directory}"
        )

    if not directory.is_dir():
        raise argparse.ArgumentTypeError(
            f"La ruta no corresponde a un directorio: {directory}"
        )

    return directory


def get_baseline_path(directory: Path, filename: str) -> Path:
    """Construye la ruta del archivo de línea base."""
    return directory / filename


def initialize_monitor(
    directory: Path,
    baseline_name: str,
) -> None:
    """Genera y guarda la primera línea base del directorio."""
    baseline_path = get_baseline_path(directory, baseline_name)

    with console.status(
        "[bold cyan]Calculando hashes SHA-256...",
        spinner="dots",
        spinner_style="bright_blue",
    ):
        baseline = build_baseline(directory)
        save_baseline(baseline, baseline_path)

    print_baseline_created(
        directory=str(directory),
        file_count=len(baseline),
        baseline_path=str(baseline_path),
    )


def scan_directory(
    directory: Path,
    baseline_name: str,
) -> None:
    """Compara el estado actual del directorio con su línea base."""
    baseline_path = get_baseline_path(directory, baseline_name)

    original_baseline = load_baseline(baseline_path)

    start_time = time.perf_counter()

    with console.status(
        "[bold cyan]Analizando archivos y verificando hashes...",
        spinner="dots",
        spinner_style="bright_blue",
    ):
        current_baseline = build_baseline(directory)

    duration = time.perf_counter() - start_time

    changes = compare_baselines(
        original=original_baseline,
        current=current_baseline,
    )

    print_scan_results(
        changes=changes,
        directory=str(directory),
        scanned_files=len(current_baseline),
        duration=duration,
    )


def build_parser() -> argparse.ArgumentParser:
    """Construye la interfaz de línea de comandos."""
    parser = argparse.ArgumentParser(
        prog="file-integrity-monitor",
        description=(
            "Detecta archivos nuevos, modificados y eliminados "
            "mediante hashes SHA-256."
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {APP_VERSION}",
    )

    parser.add_argument(
        "--baseline",
        default=DEFAULT_BASELINE_NAME,
        metavar="ARCHIVO",
        help=(
            "Nombre del archivo de línea base. "
            f"Predeterminado: {DEFAULT_BASELINE_NAME}"
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    init_parser = subparsers.add_parser(
        "init",
        help="Crea la línea base inicial de un directorio.",
    )
    init_parser.add_argument(
        "directory",
        type=validate_directory,
        help="Directorio que será monitorizado.",
    )

    scan_parser = subparsers.add_parser(
        "scan",
        help="Compara el directorio con su línea base.",
    )
    scan_parser.add_argument(
        "directory",
        type=validate_directory,
        help="Directorio que será analizado.",
    )

    return parser


def main() -> None:
    """Punto de entrada principal."""
    parser = build_parser()
    arguments = parser.parse_args()

    print_banner()
    console.print()

    try:
        if arguments.command == "init":
            initialize_monitor(
                directory=arguments.directory,
                baseline_name=arguments.baseline,
            )

        elif arguments.command == "scan":
            scan_directory(
                directory=arguments.directory,
                baseline_name=arguments.baseline,
            )

    except FileNotFoundError as error:
        console.print(
            Panel(
                str(error),
                title="[bold red]Línea base no encontrada[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)

    except PermissionError as error:
        console.print(
            Panel(
                f"No fue posible acceder a un archivo o directorio.\n\n{error}",
                title="[bold red]Permiso denegado[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)

    except ValueError as error:
        console.print(
            Panel(
                str(error),
                title="[bold red]Datos inválidos[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)

    except KeyboardInterrupt:
        console.print(
            "\n[yellow]Operación cancelada por el usuario.[/yellow]"
        )
        sys.exit(130)


if __name__ == "__main__":
    main()