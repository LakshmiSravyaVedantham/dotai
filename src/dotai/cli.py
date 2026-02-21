"""CLI interface for dotai — one config for all your AI coding tools."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from dotai import __version__
from dotai.adapters import ALL_ADAPTERS
from dotai.config import (
    add_rule,
    create_default_config,
    detect_project_info,
    get_config_path,
    read_config,
    remove_rule,
    write_config,
)
from dotai.detector import detect_tools, get_adapter_by_name

app = typer.Typer(
    name="dotai",
    help="One config for all your AI coding tools.",
    no_args_is_help=True,
    rich_markup_mode="rich",
)
console = Console()


def version_callback(value: bool) -> None:
    if value:
        console.print(f"dotai [bold cyan]{__version__}[/bold cyan]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """dotai — One config for all your AI coding tools."""


@app.command()
def init(
    project_dir: Optional[str] = typer.Option(
        None, "--dir", "-d", help="Project directory"
    ),
) -> None:
    """Initialize .ai/config.yml with auto-detected project settings."""
    base = Path(project_dir) if project_dir else Path.cwd()
    config_path = get_config_path(base)

    if config_path.exists():
        console.print(f"[yellow]Config already exists at {config_path}[/yellow]")
        overwrite = typer.confirm("Overwrite?", default=False)
        if not overwrite:
            raise typer.Exit()

    # Start with defaults, then overlay detected info
    config = create_default_config()
    detected = detect_project_info(base)

    if detected.get("name"):
        config["project"]["name"] = detected["name"]
    if detected.get("language"):
        config["project"]["language"] = detected["language"]
    if detected.get("framework"):
        config["project"]["framework"] = detected["framework"]
    if detected.get("formatting"):
        config["style"]["formatting"] = detected["formatting"]
    if detected.get("linting"):
        config["style"]["linting"] = detected["linting"]
    if detected.get("testing"):
        config["testing"]["framework"] = detected["testing"]

    write_config(config_path, config)

    lang = config["project"]["language"] or "not detected"
    fw = config["project"]["framework"] or "not detected"
    lint = config["style"]["linting"] or "not detected"
    test_fw = config["testing"]["framework"] or "not detected"
    panel_text = (
        f"[green]Created[/green] {config_path}\n\n"
        f"[dim]Project:[/dim]    {config['project']['name']}\n"
        f"[dim]Language:[/dim]   {lang}\n"
        f"[dim]Framework:[/dim]  {fw}\n"
        f"[dim]Linter:[/dim]     {lint}\n"
        f"[dim]Tests:[/dim]      {test_fw}"
    )
    console.print(
        Panel(
            panel_text,
            title="[bold green]dotai init[/bold green]",
            border_style="green",
        )
    )
    console.print("\nNext: [bold]dotai sync[/bold] to generate tool configs")


@app.command()
def sync(
    project_dir: Optional[str] = typer.Option(
        None, "--dir", "-d", help="Project directory"
    ),
    tool: Optional[str] = typer.Option(
        None, "--tool", "-t", help="Sync only a specific tool"
    ),
) -> None:
    """Sync .ai/config.yml to all AI tool config files."""
    base = Path(project_dir) if project_dir else Path.cwd()
    config_path = get_config_path(base)

    if not config_path.exists():
        console.print(
            "[red]No .ai/config.yml found. Run [bold]dotai init[/bold] first.[/red]"
        )
        raise typer.Exit(1)

    config = read_config(config_path)
    if not config:
        console.print("[red]Config is empty.[/red]")
        raise typer.Exit(1)

    adapters_to_run = []
    if tool:
        adapter = get_adapter_by_name(tool)
        if not adapter:
            console.print(f"[red]Unknown tool: {tool}[/red]")
            console.print("Available: " + ", ".join(a().name for a in ALL_ADAPTERS))
            raise typer.Exit(1)
        adapters_to_run = [adapter]
    else:
        adapters_to_run = [cls() for cls in ALL_ADAPTERS]

    synced = []
    for adapter in adapters_to_run:
        path = adapter.write(base, config)
        synced.append((adapter.name, adapter.description, path))

    table = Table(title="Synced configs", show_lines=False)
    table.add_column("Tool", style="cyan bold")
    table.add_column("File", style="green")
    table.add_column("Status", style="bold")

    for name, desc, path in synced:
        table.add_row(desc, str(path.relative_to(base)), "[green]written[/green]")

    console.print(table)
    console.print(f"\n[green]Synced {len(synced)} tool(s) from {config_path}[/green]")


@app.command()
def status(
    project_dir: Optional[str] = typer.Option(
        None, "--dir", "-d", help="Project directory"
    ),
) -> None:
    """Show which AI tool configs exist and their sync status."""
    base = Path(project_dir) if project_dir else Path.cwd()
    config_path = get_config_path(base)

    has_config = config_path.exists()

    table = Table(title="AI Tool Config Status", show_lines=False)
    table.add_column("Tool", style="bold")
    table.add_column("File", style="dim")
    table.add_column("Status")

    tools = detect_tools(base)
    for t in tools:
        if t.exists:
            status_str = "[green]exists[/green]"
        else:
            status_str = "[dim]not found[/dim]"
        table.add_row(t.description, t.file_name, status_str)

    console.print(table)

    if has_config:
        console.print(f"\n[green]Central config:[/green] {config_path}")
    else:
        console.print(
            "\n[yellow]No .ai/config.yml found.[/yellow] Run [bold]dotai init[/bold]"
        )


@app.command()
def add(
    rule: str = typer.Argument(..., help="Rule to add"),
    project_dir: Optional[str] = typer.Option(
        None, "--dir", "-d", help="Project directory"
    ),
) -> None:
    """Add a rule to .ai/config.yml."""
    base = Path(project_dir) if project_dir else Path.cwd()
    config_path = get_config_path(base)

    if not config_path.exists():
        console.print("[red]No config found. Run [bold]dotai init[/bold] first.[/red]")
        raise typer.Exit(1)

    config = read_config(config_path)
    add_rule(config, rule)
    write_config(config_path, config)
    console.print(f"[green]Added rule:[/green] {rule}")


@app.command()
def remove(
    rule: str = typer.Argument(..., help="Rule to remove"),
    project_dir: Optional[str] = typer.Option(
        None, "--dir", "-d", help="Project directory"
    ),
) -> None:
    """Remove a rule from .ai/config.yml."""
    base = Path(project_dir) if project_dir else Path.cwd()
    config_path = get_config_path(base)

    if not config_path.exists():
        console.print("[red]No config found.[/red]")
        raise typer.Exit(1)

    config = read_config(config_path)
    if remove_rule(config, rule):
        write_config(config_path, config)
        console.print(f"[green]Removed rule:[/green] {rule}")
    else:
        console.print(f"[yellow]Rule not found:[/yellow] {rule}")


@app.command()
def rules(
    project_dir: Optional[str] = typer.Option(
        None, "--dir", "-d", help="Project directory"
    ),
) -> None:
    """List all rules in .ai/config.yml."""
    base = Path(project_dir) if project_dir else Path.cwd()
    config_path = get_config_path(base)

    if not config_path.exists():
        console.print("[red]No config found. Run [bold]dotai init[/bold] first.[/red]")
        raise typer.Exit(1)

    config = read_config(config_path)
    rule_list = config.get("rules", [])

    if not rule_list:
        console.print("[yellow]No rules defined.[/yellow]")
        return

    console.print("[bold]Rules:[/bold]\n")
    for i, rule in enumerate(rule_list, 1):
        console.print(f"  {i}. {rule}")


@app.command(name="import")
def import_config(
    tool: str = typer.Argument(..., help="Tool to import from (claude, cursor, etc.)"),
    project_dir: Optional[str] = typer.Option(
        None, "--dir", "-d", help="Project directory"
    ),
) -> None:
    """Import rules from an existing tool config into .ai/config.yml."""
    base = Path(project_dir) if project_dir else Path.cwd()
    config_path = get_config_path(base)

    adapter = get_adapter_by_name(tool)
    if not adapter:
        console.print(f"[red]Unknown tool: {tool}[/red]")
        raise typer.Exit(1)

    existing = adapter.read_existing(base)
    if not existing:
        console.print(f"[yellow]No {adapter.file_name} found to import from.[/yellow]")
        raise typer.Exit(1)

    # Read or create config
    config = (
        read_config(config_path) if config_path.exists() else create_default_config()
    )

    # Extract lines that look like rules (bullet points)
    imported = 0
    for line in existing.splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") and len(stripped) > 5:
            rule = stripped[2:].strip()
            # Skip markdown formatting artifacts
            if rule.startswith("**") or rule.startswith("`") or rule.startswith("["):
                continue
            if rule not in config.get("rules", []):
                add_rule(config, rule)
                imported += 1

    write_config(config_path, config)
    console.print(
        f"[green]Imported {imported} rule(s) from {adapter.file_name}[/green]"
    )


@app.command()
def diff(
    project_dir: Optional[str] = typer.Option(
        None, "--dir", "-d", help="Project directory"
    ),
) -> None:
    """Show what would change on next sync."""
    base = Path(project_dir) if project_dir else Path.cwd()
    config_path = get_config_path(base)

    if not config_path.exists():
        console.print("[red]No config found. Run [bold]dotai init[/bold] first.[/red]")
        raise typer.Exit(1)

    config = read_config(config_path)

    for adapter_cls in ALL_ADAPTERS:
        adapter = adapter_cls()
        new_content = adapter.generate(config)
        existing = adapter.read_existing(base)

        desc = adapter.description
        fname = adapter.file_name
        if existing is None:
            status_msg = "[green]new file[/green]"
        elif existing == new_content:
            status_msg = "[dim]up to date[/dim]"
        else:
            status_msg = "[yellow]will update[/yellow]"
        console.print(f"[cyan]{desc}[/cyan] ({fname}): {status_msg}")


@app.command()
def tools() -> None:
    """List all supported AI coding tools."""
    table = Table(title="Supported AI Tools", show_lines=False)
    table.add_column("Tool", style="cyan bold")
    table.add_column("Config File", style="green")
    table.add_column("Name", style="dim")

    for adapter_cls in ALL_ADAPTERS:
        adapter = adapter_cls()
        table.add_row(adapter.description, adapter.file_name, adapter.name)

    console.print(table)
    console.print(f"\n[dim]{len(ALL_ADAPTERS)} tools supported[/dim]")


if __name__ == "__main__":
    app()
