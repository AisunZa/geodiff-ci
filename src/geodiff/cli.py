import typer

from geodiff.compare import (
    compare_datasets,
)
from geodiff.report import (
    render_terminal_report,
    write_json_report,
)


app = typer.Typer(
    help=(
        "Geospatial regression testing "
        "for data pipelines."
    )
)


@app.callback()
def main():
    """GeoDiff CI command-line interface."""

    pass


@app.command()
def version():
    """Show the current GeoDiff CI version."""

    typer.echo(
        "GeoDiff CI 0.1.0"
    )


@app.command()
def compare(
    baseline: str,
    candidate: str,
    max_feature_loss: float = typer.Option(
        0.0,
        "--max-feature-loss",
        help=(
            "Maximum allowed feature loss "
            "as a percentage."
        ),
        min=0.0,
        max=100.0,
    ),
    max_null_increase: int = typer.Option(
        0,
        "--max-null-increase",
        help=(
            "Maximum allowed increase "
            "in null geometries."
        ),
        min=0,
    ),
    max_invalid_increase: int = typer.Option(
        0,
        "--max-invalid-increase",
        help=(
            "Maximum allowed increase "
            "in invalid geometries."
        ),
        min=0,
    ),
    json_output: str | None = typer.Option(
        None,
        "--json-output",
        "-j",
        help=(
            "Write the comparison report "
            "to a JSON file."
        ),
    ),
):
    """Compare a candidate dataset against a baseline."""

    try:
        results = compare_datasets(
            baseline,
            candidate,
            max_feature_loss=(
                max_feature_loss
            ),
            max_null_increase=(
                max_null_increase
            ),
            max_invalid_increase=(
                max_invalid_increase
            ),
        )

    except (
        FileNotFoundError,
        ValueError,
    ) as error:

        typer.echo(
            f"Error: {error}"
        )

        raise typer.Exit(
            code=2
        )

    render_terminal_report(
        results
    )

    if json_output is not None:

        report_path = (
            write_json_report(
                results,
                json_output,
            )
        )

        typer.echo(
            f"\nJSON report saved to: "
            f"{report_path}"
        )

    if not results["passed"]:
        raise typer.Exit(
            code=1
        )