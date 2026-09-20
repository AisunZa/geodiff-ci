GeoDiff CI






Geospatial regression testing for data pipelines.

GeoDiff CI compares a baseline geospatial dataset with a candidate dataset and detects potentially breaking changes before they reach production.

Think of it as a lightweight regression-testing layer for spatial data: useful in ETL pipelines, data-processing workflows, and CI/CD systems where changes in geometry, schema, or feature counts need to be detected automatically.

Why GeoDiff?

Traditional software projects have unit tests to detect regressions in code.

Geospatial pipelines also need regression checks for their data.

A processing change can unexpectedly:

remove features
drop columns
change the CRS
introduce invalid geometries
introduce missing geometries
change geometry types

GeoDiff makes these changes visible and can fail a CI pipeline when configured tolerances are exceeded.

Features

GeoDiff currently checks:

Feature count changes
Feature-loss percentage
Schema changes
Removed and added columns
CRS changes
Geometry type changes
Missing/null geometries
Invalid geometries
Configurable regression thresholds
Machine-readable JSON reports
CI-friendly exit codes
Colored terminal reports
Supported formats

GeoDiff can currently load:

GeoJSON
GeoParquet
GeoPackage
ESRI Shapefile
JSON datasets supported by GeoPandas
Installation

Clone the repository:

git clone https://github.com/AisunZa/geodiff-ci.git
cd geodiff-ci

Create a virtual environment:

python -m venv .venv

Activate it.

Windows PowerShell
.venv\Scripts\Activate.ps1
Linux / macOS
source .venv/bin/activate

Install GeoDiff:

python -m pip install -e .

For development and testing:

python -m pip install -e ".[dev]"
Quick start

Compare two geospatial datasets:

geodiff compare baseline.geojson candidate.geojson

Example:

geodiff compare examples/baseline.geojson examples/candidate.geojson

GeoDiff produces a regression report similar to:

GeoDiff Regression Report

Check                Baseline    Candidate    Details                       Status
Feature count        2           1            Loss: 50% | Allowed: 0%       FAIL
Schema               -           -            No column changes             PASS
CRS                  EPSG:4326   EPSG:4326    Coordinate reference system   PASS
Geometry types       Polygon     Polygon      Geometry type consistency     PASS
Null geometries      0           0            Allowed increase: 0           PASS
Invalid geometries   0           0            Allowed increase: 0           PASS

FAILED — One or more regressions exceeded the configured thresholds.
Configurable thresholds

Not every dataset change should fail a pipeline.

GeoDiff allows acceptable tolerances to be configured.

Allow feature loss

Allow up to 5% feature loss:

geodiff compare baseline.geojson candidate.geojson \
  --max-feature-loss 5

For example, the sample candidate contains 50% fewer features than the baseline.

This fails:

geodiff compare examples/baseline.geojson examples/candidate.geojson

This passes because the loss is explicitly allowed:

geodiff compare examples/baseline.geojson examples/candidate.geojson \
  --max-feature-loss 50
Allow new null geometries
geodiff compare baseline.geojson candidate.geojson \
  --max-null-increase 2
Allow new invalid geometries
geodiff compare baseline.geojson candidate.geojson \
  --max-invalid-increase 1

Thresholds can be combined:

geodiff compare baseline.geojson candidate.geojson \
  --max-feature-loss 5 \
  --max-null-increase 1 \
  --max-invalid-increase 0
JSON reports

GeoDiff can save comparison results as JSON:

geodiff compare baseline.geojson candidate.geojson \
  --json-output reports/result.json

Example structure:

{
  "feature_count": {
    "baseline": 2,
    "candidate": 1,
    "difference": -1,
    "loss_percent": 50.0,
    "allowed_loss_percent": 0.0,
    "passed": false
  },
  "passed": false
}

This makes GeoDiff output suitable for downstream CI/CD tools and automated reporting.

Exit codes

GeoDiff uses CI-friendly process exit codes:

Exit code	Meaning
0	Comparison passed
1	A regression exceeded configured thresholds
2	Input or execution error

This means GeoDiff can directly act as a quality gate inside automated pipelines.

GitHub Actions

The repository tests GeoDiff automatically on:

Python 3.11
Python 3.12
Python 3.13

The workflow runs on pushes and pull requests to main.

A pipeline can also use GeoDiff itself as a validation step:

- name: Check geospatial regression
  run: >
    geodiff compare
    data/baseline.geojson
    data/candidate.geojson
    --max-feature-loss 2

If the configured tolerance is exceeded, GeoDiff exits with status 1 and the workflow fails.

Running the tests

Run:

pytest

For detailed output:

pytest -v

The test suite covers feature-count regressions, schema changes, CRS changes, geometry-type changes, invalid and missing geometries, and configurable thresholds.

Project structure
geodiff-ci/
├── .github/
│   └── workflows/
│       └── ci.yml
├── examples/
│   ├── baseline.geojson
│   └── candidate.geojson
├── src/
│   └── geodiff/
│       ├── __init__.py
│       ├── cli.py
│       ├── compare.py
│       └── report.py
├── tests/
│   ├── test_compare.py
│   └── test_report.py
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
Design principles

GeoDiff is intentionally small and focused.

The project favors:

explicit regression rules
deterministic comparisons
useful CI exit codes
testable comparison functions
machine-readable output
minimal infrastructure requirements

It is designed as a developer tool rather than a dashboard or geospatial visualization platform.

Roadmap

Potential future checks include:

Bounding-box / spatial extent regression
Duplicate feature ID detection
Geometry area and length drift
Attribute type changes
Numeric attribute distribution changes
Config-file based thresholds
Markdown CI reports
Per-check enable/disable controls
Additional geospatial formats
Technology
Python
GeoPandas
Shapely
PyArrow
Typer
Rich
Pytest
GitHub Actions
License

MIT License.