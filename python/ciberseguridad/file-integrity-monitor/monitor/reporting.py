from __future__ import annotations

from dataclasses import dataclass

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from monitor.baseline import Baseline


console = Console()


@dataclass(frozen=True)
class IntegrityChanges:
    """Representa las diferencias entre dos estados de un directorio."""

    added: list[str]
    modified: list[str]
    deleted: list[str]

    @property
    def total(self) -> int:
        """Devuelve la cantidad total de cambios detectados."""
        return len(self.added) + len(self.modified) + len(self.deleted)

    @property
    def is_clean(self) -> bool:
        """Indica si no se detectaron cambios."""
        return self.total == 0


def compare_baselines(
    original: Baseline,
    current: Baseline,
) -> IntegrityChanges:
    """Compara la línea base original con el estado actual."""
    original_paths = set(original)
    current_paths = set(current)

    added = sorted(current_paths - original_paths)
    deleted = sorted(original_paths - current_paths)

    modified = sorted(
        path
        for path in original_paths & current_paths
        if original[path] != current[path]
    )

    return IntegrityChanges(
        added=added,
        modified=modified,
        deleted=deleted,
    )


def print_banner() -> None:
    """Muestra el encabezado principal de la aplicación."""
    console.print(
        Panel.fit(
            "[bold cyan]File Integrity Monitor[/bold cyan]\n"
            "[dim]SHA-256 change detection · v1.0.0[/dim]",
            border_style="bright_blue",
            box=box.DOUBLE,
            padding=(1, 5),
        )
    )


def print_baseline_created(
    directory: str,
    file_count: int,
    baseline_path: str,
) -> None:
    """Muestra el resumen de una línea base creada."""
    summary = Table.grid(padding=(0, 2))
    summary.add_column(style="bold cyan", justify="right")
    summary.add_column()

    summary.add_row("Directorio", directory)
    summary.add_row("Archivos registrados", str(file_count))
    summary.add_row("Línea base", baseline_path)
    summary.add_row("Estado", "[bold green]Creada correctamente[/bold green]")

    console.print(
        Panel(
            summary,
            title="[bold green]Inicialización completada[/bold green]",
            border_style="green",
            box=box.ROUNDED,
        )
    )


def create_changes_table(changes: IntegrityChanges) -> Table:
    """Construye una tabla Rich con todos los cambios detectados."""
    table = Table(
        title="Cambios detectados",
        box=box.ROUNDED,
        border_style="bright_blue",
        header_style="bold white on blue",
        show_lines=True,
        expand=True,
    )

    table.add_column("#", justify="right", style="dim", width=4)
    table.add_column("Estado", justify="center", width=14)
    table.add_column("Archivo", style="white")

    row_number = 1

    for file_path in changes.added:
        table.add_row(
            str(row_number),
            "[bold green]NUEVO[/bold green]",
            file_path,
        )
        row_number += 1

    for file_path in changes.modified:
        table.add_row(
            str(row_number),
            "[bold yellow]MODIFICADO[/bold yellow]",
            file_path,
        )
        row_number += 1

    for file_path in changes.deleted:
        table.add_row(
            str(row_number),
            "[bold red]ELIMINADO[/bold red]",
            file_path,
        )
        row_number += 1

    return table


def print_scan_results(
    changes: IntegrityChanges,
    directory: str,
    scanned_files: int,
    duration: float,
) -> None:
    """Muestra los resultados y el resumen del análisis."""
    if changes.is_clean:
        console.print(
            Panel(
                "[bold green]No se detectaron modificaciones.[/bold green]\n\n"
                "Los archivos coinciden con la línea base.",
                title="[bold green]Integridad verificada[/bold green]",
                border_style="green",
                box=box.ROUNDED,
            )
        )
    else:
        console.print(create_changes_table(changes))

    summary = Table.grid(padding=(0, 2))
    summary.add_column(style="bold cyan", justify="right")
    summary.add_column()

    summary.add_row("Directorio", directory)
    summary.add_row("Archivos analizados", str(scanned_files))
    summary.add_row("Nuevos", f"[green]{len(changes.added)}[/green]")
    summary.add_row(
        "Modificados",
        f"[yellow]{len(changes.modified)}[/yellow]",
    )
    summary.add_row(
        "Eliminados",
        f"[red]{len(changes.deleted)}[/red]",
    )
    summary.add_row("Cambios totales", str(changes.total))
    summary.add_row("Duración", f"{duration:.3f} segundos")

    status = (
        "[bold green]Sin cambios[/bold green]"
        if changes.is_clean
        else "[bold yellow]Revisión requerida[/bold yellow]"
    )
    summary.add_row("Estado", status)

    console.print()
    console.print(
        Panel(
            summary,
            title="[bold]Resumen del análisis[/bold]",
            border_style="cyan",
            box=box.ROUNDED,
        )
    )