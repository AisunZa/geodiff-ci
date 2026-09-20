import json
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel


console = Console()


def write_json_report(results, output_path: str):
    """Write comparison results to a JSON file."""

    path = Path(output_path)

    if path.parent != Path("."):
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            results,
            file,
            indent=2,
        )

    return path


def status_text(passed: bool) -> str:
    """Return a formatted PASS/FAIL status."""

    if passed:
        return "[bold green]PASS[/bold green]"

    return "[bold red]FAIL[/bold red]"


def render_terminal_report(results):
    """Render a human-readable GeoDiff comparison report."""

    table = Table(
        title="GeoDiff Regression Report",
        show_header=True,
        header_style="bold",
    )

    table.add_column(
        "Check",
        style="bold",
    )

    table.add_column(
        "Baseline",
    )

    table.add_column(
        "Candidate",
    )

    table.add_column(
        "Details",
    )

    table.add_column(
        "Status",
        justify="center",
    )

    feature_count = results[
        "feature_count"
    ]

    table.add_row(
        "Feature count",
        str(feature_count["baseline"]),
        str(feature_count["candidate"]),
        (
            f"Loss: "
            f"{feature_count['loss_percent']}% "
            f"| Allowed: "
            f"{feature_count['allowed_loss_percent']}%"
        ),
        status_text(
            feature_count["passed"]
        ),
    )

    schema = results["schema"]

    schema_details = []

    if schema["added"]:
        schema_details.append(
            "Added: "
            + ", ".join(
                schema["added"]
            )
        )

    if schema["removed"]:
        schema_details.append(
            "Removed: "
            + ", ".join(
                schema["removed"]
            )
        )

    if not schema_details:
        schema_details.append(
            "No column changes"
        )

    table.add_row(
        "Schema",
        "-",
        "-",
        " | ".join(schema_details),
        status_text(
            schema["passed"]
        ),
    )

    crs = results["crs"]

    table.add_row(
        "CRS",
        str(crs["baseline"]),
        str(crs["candidate"]),
        "Coordinate reference system",
        status_text(
            crs["passed"]
        ),
    )

    geometry_types = results[
        "geometry_types"
    ]

    table.add_row(
        "Geometry types",
        ", ".join(
            geometry_types["baseline"]
        )
        or "None",
        ", ".join(
            geometry_types["candidate"]
        )
        or "None",
        "Geometry type consistency",
        status_text(
            geometry_types["passed"]
        ),
    )

    null_geometries = results[
        "null_geometries"
    ]

    table.add_row(
        "Null geometries",
        str(
            null_geometries[
                "baseline"
            ]
        ),
        str(
            null_geometries[
                "candidate"
            ]
        ),
        (
            f"Allowed increase: "
            f"{null_geometries['allowed_increase']}"
        ),
        status_text(
            null_geometries["passed"]
        ),
    )

    invalid_geometries = results[
        "invalid_geometries"
    ]

    table.add_row(
        "Invalid geometries",
        str(
            invalid_geometries[
                "baseline"
            ]
        ),
        str(
            invalid_geometries[
                "candidate"
            ]
        ),
        (
            f"Allowed increase: "
            f"{invalid_geometries['allowed_increase']}"
        ),
        status_text(
            invalid_geometries[
                "passed"
            ]
        ),
    )

    console.print()
    console.print(table)

    if results["passed"]:
        summary = Panel(
            "[bold green]"
            "PASSED — No unacceptable regressions detected."
            "[/bold green]",
            title="Result",
            border_style="green",
        )

    else:
        summary = Panel(
            "[bold red]"
            "FAILED — One or more regressions exceeded "
            "the configured thresholds."
            "[/bold red]",
            title="Result",
            border_style="red",
        )

    console.print(summary)