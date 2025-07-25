"""Main CLI for clfits."""

import sys
from pathlib import Path
from typing import Optional, Union

import typer

# Use Typer's built-in echo function for output. This ensures that all
# CLI output is routed through Click's testing helpers, allowing
# typer.testing.CliRunner to capture `stdout`/`stderr` reliably during
# tests.
from clfits import __version__
from clfits.export import Format, export_header
from clfits.io import read_header, write_header
from clfits.search import search_header

app = typer.Typer(
    add_completion=False,
    rich_markup_mode="markdown",
    context_settings={"help_option_names": ["-h", "--help"]},
)


def version_callback(value: bool) -> None:
    """Print the version of the package and exit."""
    if value:
        typer.echo(f"clfits version: {__version__}")
        raise typer.Exit()


HDU = Union[int, str]


def _get_hdu(hdu_str: str) -> HDU:
    """Convert a string HDU identifier to an int if possible."""
    return int(hdu_str) if hdu_str.isdigit() else hdu_str


# Reusable Typer option for specifying the HDU
HDUOption = typer.Option(
    "0",
    "--hdu",
    "-h",
    help="The Header Data Unit (HDU) to operate on, specified by its 0-based index or name.",
)


@app.command()
def view(
    fits_file: Path = typer.Argument(..., help="The FITS file to view."),
    hdu: str = HDUOption,
) -> None:
    """View the header of a FITS file."""
    try:
        header = read_header(fits_file, _get_hdu(hdu))
        # Pad keywords for alignment
        for card in header.cards:
            keyword = card.keyword.ljust(8)
            value = f"= '{card.value}'" if isinstance(card.value, str) else f"= {card.value}"
            comment = f" / {card.comment}" if card.comment else ""
            typer.echo(f"{keyword}{value}{comment}")
    except (FileNotFoundError, IndexError, KeyError, OSError) as e:
        typer.secho(str(e), fg=typer.colors.RED, bold=True, err=True)
        raise SystemExit(1)


@app.command()
def get(
    fits_file: Path = typer.Argument(..., help="The FITS file to read from."),
    keyword: str = typer.Argument(..., help="The keyword to retrieve."),
    hdu: str = HDUOption,
) -> None:
    """Get the value of a specific header keyword."""
    try:
        header = read_header(fits_file, _get_hdu(hdu))
        value = header.get(keyword)
        if value is None:
            typer.secho(
                f"Error: Keyword '{keyword}' not found in '{fits_file}'.", fg=typer.colors.RED, bold=True, err=True
            )
            raise SystemExit(1)
        typer.echo(value)
    except (FileNotFoundError, IndexError, KeyError, OSError) as e:
        typer.secho(str(e), fg=typer.colors.RED, bold=True, err=True)
        raise SystemExit(1)


@app.command()
def set(
    fits_file: Path = typer.Argument(..., help="The FITS file to modify."),
    keyword: str = typer.Argument(..., help="The keyword to set or modify."),
    value: str = typer.Argument(..., help="The value to assign to the keyword."),
    comment: Optional[str] = typer.Option(None, "--comment", "-c", help="An optional comment for the keyword."),
    hdu: str = HDUOption,
) -> None:
    """Set a keyword's value, with an optional comment."""
    try:
        header = read_header(fits_file, _get_hdu(hdu))
        header[keyword] = (value, comment) if comment else value
        write_header(fits_file, header, _get_hdu(hdu))
        typer.secho(f"Success: Set '{keyword}' to '{value}' in '{fits_file}'.", fg=typer.colors.GREEN, bold=True)
    except (FileNotFoundError, IndexError, KeyError, OSError) as e:
        typer.secho(str(e), fg=typer.colors.RED, bold=True, err=True)
        raise SystemExit(1)


# Register this function under the short command name 'del' to match tests.
@app.command(name="del")
def delete(
    fits_file: Path = typer.Argument(..., help="The FITS file to modify."),
    keyword: str = typer.Argument(..., help="The keyword to delete."),
    hdu: str = HDUOption,
) -> None:
    """Delete a keyword from the header."""
    try:
        header = read_header(fits_file, _get_hdu(hdu))
        if keyword not in header:
            typer.secho(
                f"Warning: Keyword '{keyword}' not found in '{fits_file}'.", fg=typer.colors.YELLOW, bold=True, err=True
            )
            raise SystemExit(0)
        del header[keyword]
        write_header(fits_file, header, _get_hdu(hdu))
        typer.secho(f"Success: Deleted '{keyword}' from '{fits_file}'.", fg=typer.colors.GREEN, bold=True)
    except (FileNotFoundError, IndexError, KeyError, OSError) as e:
        typer.secho(str(e), fg=typer.colors.RED, bold=True, err=True)
        raise SystemExit(1)


@app.command()
def export(
    fits_file: Path = typer.Argument(..., dir_okay=False, help="The input FITS file."),
    format: Optional[Format] = typer.Option(
        None,
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format. Inferred from --output filename if not provided.",
    ),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Path to save the output file.", dir_okay=False, writable=True
    ),
    hdu: str = HDUOption,
) -> None:
    """Export the FITS header to a specified format (JSON, YAML, or CSV)."""
    # Determine the format
    if format is None:
        if output_file is None:
            typer.secho(
                "Error: --format is required when not writing to an output file.",
                fg=typer.colors.RED,
                bold=True,
                err=True,
            )
            raise SystemExit(1)

        # Infer format from filename extension
        suffix_map = {".json": Format.JSON, ".yml": Format.YAML, ".yaml": Format.YAML, ".csv": Format.CSV}
        format = suffix_map.get(output_file.suffix.lower())
        if format is None:
            typer.secho(
                f"Error: Could not infer format from '{output_file.name}'. Please use --format.",
                fg=typer.colors.RED,
                bold=True,
                err=True,
            )
            raise SystemExit(1)

    try:
        header = read_header(fits_file, _get_hdu(hdu))
        export_header(header, format, output_file)
        if output_file:
            typer.secho(f"Success: Header exported to '{output_file}'.", fg=typer.colors.GREEN, bold=True)
    except (FileNotFoundError, IndexError, KeyError, OSError) as e:
        typer.secho(str(e), fg=typer.colors.RED, bold=True, err=True)
        raise SystemExit(1)


@app.command()
def search(
    fits_file: Path = typer.Argument(help="The FITS file to search."),
    key_pattern: Optional[str] = typer.Option(None, "--key", "-k", help="Glob pattern for the keyword."),
    value_pattern: Optional[str] = typer.Option(None, "--value", "-v", help="Glob pattern for the value."),
    case_sensitive: bool = typer.Option(False, "--case-sensitive", "-c", help="Perform a case-sensitive search."),
    hdu: str = HDUOption,
) -> None:
    """Search for keywords in a FITS header by pattern."""
    if key_pattern is None and value_pattern is None:
        typer.secho(
            "Error: At least one of --key or --value must be provided.", fg=typer.colors.RED, bold=True, err=True
        )
        raise SystemExit(1)

    try:
        header = read_header(fits_file, _get_hdu(hdu))
        matches = search_header(header, key_pattern, value_pattern, case_sensitive)
        if not matches:
            typer.secho("No matching keywords found.", fg=typer.colors.YELLOW)
            return

        for card in matches.cards:
            keyword = card.keyword.ljust(8)
            value = f"= '{card.value}'" if isinstance(card.value, str) else f"= {card.value}"
            comment = f" / {card.comment}" if card.comment else ""
            typer.echo(f"{keyword}{value}{comment}")
    except (FileNotFoundError, IndexError, KeyError, OSError) as e:
        typer.secho(str(e), fg=typer.colors.RED, bold=True, err=True)
        raise SystemExit(1)


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
) -> None:
    """Manage FITS headers from the command line."""
    pass


if __name__ == "__main__":
    sys.exit(app())
