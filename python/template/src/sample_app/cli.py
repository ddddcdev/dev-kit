"""Command-line entry point. Every command works non-interactively and offers --json."""

import json

import typer
from rich.console import Console

app = typer.Typer(no_args_is_help=True, add_completion=False)
console = Console()


@app.callback()
def root() -> None:
    """One line: what this tool does."""


@app.command()
def hello(
    name: str = typer.Option("world", "--name", "-n", help="Who to greet."),
    as_json: bool = typer.Option(False, "--json", help="Machine-readable output."),
) -> None:
    """Greet someone (example command; replace it)."""
    message = f"hello, {name}"
    if as_json:
        print(json.dumps({"message": message}))
    else:
        console.print(message)


def main() -> None:
    app()
