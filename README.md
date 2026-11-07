# GeoDiff CI

[![CI](https://github.com/AisunZa/geodiff-ci/actions/workflows/ci.yml/badge.svg)](https://github.com/AisunZa/geodiff-ci/actions/workflows/ci.yml)

**Geospatial regression testing for data pipelines.**

GeoDiff CI is a Python command-line tool that compares a **baseline** geospatial dataset with a **candidate** dataset to detect changes that could break a data-processing workflow. It checks feature counts, schema, coordinate reference systems (CRS), geometry quality, and spatial extent, and returns exit codes suitable for CI pipelines.

**Start here:** [Quick start](#quick-start) · [Checks](#what-geodiff-checks) · [Thresholds](#configurable-thresholds) · [GitHub Actions](#github-actions) · [Development](#development) · [Changelog](CHANGELOG.md)

## Why GeoDiff?

Traditional software projects use tests to detect code regressions. Geospatial pipelines also need checks for **data regressions**. A processing change can unexpectedly remove features or columns, alter the CRS, introduce invalid or missing geometries, change geometry types, or reduce geographic coverage.

GeoDiff makes these changes visible and can fail a pipeline when a configured threshold is exceeded.

## Install directly from GitHub

Requires Python 3.11+ and Git. In an activated virtual environment, run:

```bash
python -m pip install "geodiff-ci @ git+https://github.com/AisunZa/geodiff-ci.git@v0.1.0"
geodiff version
```

This installs the tagged `v0.1.0` release without manually cloning the repository. For sample datasets, testing, or development, follow the local installation instructions below.

GeoDiff CI is not currently published to PyPI.

## Quick start

Requires **Python 3.11+**.

```bash
git clone https://github.com/AisunZa/geodiff-ci.git
cd geodiff-ci
python -m venv .venv
```

Activate the virtual environment:

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

Install the package and run the included comparison example:

```bash
python -m pip install -e .
geodiff compare examples/baseline.geojson examples/candidate.geojson
```

The example deliberately contains fewer features in the candidate dataset, so **a failure report and exit code `1` are expected** with default thresholds. To allow the example's 50% feature loss:

```bash
geodiff compare examples/baseline.geojson examples/candidate.geojson --max-feature-loss 50
```

> **Note:** This is a local-install workflow. The repository does not claim that `geodiff-ci` is published to PyPI.

## Use GeoDiff CI in Python

You can also use GeoDiff CI inside a Python script, without running a terminal command for each comparison.

After installing the package, run this example from the repository root:

```python
from geodiff.compare import compare_datasets

results = compare_datasets(
    "examples/baseline.geojson",
    "examples/candidate.geojson",
    max_feature_loss=50,
)

print("Comparison passed:", results["passed"])
print("Feature loss (%):", results["feature_count"]["loss_percent"])
```

The sample candidate dataset contains 50% fewer features. The example allows that loss explicitly, so the feature-loss check passes. Without the allowance, the default check would flag the missing features.

The current Python functions are importable from `geodiff.compare`; a simplified, stable public API is not yet defined.

## What GeoDiff checks

| Check | What it detects |
|---|---|
| Feature count | Added or removed features |
| Feature-loss percentage | Loss exceeding the allowed percentage |
| Schema | Added or removed columns |
| CRS | Coordinate reference system changes |
| Geometry type | Changes in geometry types |
| Null geometries | Increase in missing geometries |
| Invalid geometries | Increase in invalid shapes |
| Spatial extent | Baseline bounding-box coverage by the candidate |

**Other capabilities:** configurable thresholds, terminal reports, machine-readable JSON output, and CI-friendly exit codes.

### Supported input formats

- GeoJSON
- GeoParquet
- GeoPackage
- ESRI Shapefile
- Other JSON datasets supported by GeoPandas

## Example regression report

Comparing the included sample files without changing the default thresholds produces a report similar to:

```text
GeoDiff Regression Report

Check                Baseline         Candidate        Details                        Status
Feature count        2                1                Loss: 50% | Allowed: 0%        FAIL
Schema               -                -                No column changes              PASS
CRS                  EPSG:4326        EPSG:4326        Coordinate reference system    PASS
Geometry types       Polygon          Polygon          Geometry type consistency      PASS
Null geometries      0                0                Allowed increase: 0            PASS
Invalid geometries   0                0                Allowed increase: 0            PASS
Spatial extent       [0,0,3,3]        [0,0,1,1]        Coverage: 11.11%               PASS

FAILED — One or more regressions exceeded the configured thresholds.
```

## Configurable thresholds

Not every dataset change should fail a pipeline. GeoDiff lets you define acceptable tolerances.

### Feature loss

Allow up to 5% feature loss:

```bash
geodiff compare baseline.geojson candidate.geojson --max-feature-loss 5
```

The included sample candidate has 50% fewer features than its baseline. It fails with the defaults, but passes the **feature-loss check** when that amount is explicitly allowed:

```bash
geodiff compare examples/baseline.geojson examples/candidate.geojson --max-feature-loss 50
```

### Null and invalid geometries

Allow one additional missing geometry or one additional invalid geometry:

```bash
geodiff compare baseline.geojson candidate.geojson \
  --max-null-increase 1 \
  --max-invalid-increase 1
```

### Spatial extent regression

Feature counts alone do not establish that a dataset covers the expected geographic area. GeoDiff compares the **bounding boxes** of the baseline and candidate datasets.

For example:

```text
Baseline bounding box:  [0, 0, 3, 3]
Candidate bounding box: [0, 0, 1, 1]
Coverage: 11.11%
```

Require at least 90% coverage of the baseline bounding box:

```bash
geodiff compare baseline.geojson candidate.geojson --min-bbox-coverage 90
```

> **Important:** Bounding-box overlap is an approximation of geographic extent, not an exact comparison of the geometries' covered areas. Enforcement is **off by default**; without `--min-bbox-coverage`, GeoDiff reports coverage but does not fail specifically because of it.

### Combine thresholds

```bash
geodiff compare baseline.geojson candidate.geojson \
  --max-feature-loss 5 \
  --max-null-increase 1 \
  --max-invalid-increase 0 \
  --min-bbox-coverage 95
```

## JSON reports

Save a comparison as machine-readable JSON:

```bash
geodiff compare baseline.geojson candidate.geojson \
  --json-output reports/result.json
```

An example of the report structure is:

```json
{
  "feature_count": {
    "baseline": 2,
    "candidate": 1,
    "difference": -1,
    "loss_percent": 50.0,
    "allowed_loss_percent": 0.0,
    "passed": false
  },
  "spatial_extent": {
    "baseline": [0.0, 0.0, 3.0, 3.0],
    "candidate": [0.0, 0.0, 1.0, 1.0],
    "coverage_percent": 11.11,
    "required_coverage_percent": 0.0,
    "passed": true
  },
  "passed": false
}
```

This is a **simplified example** showing selected fields, not necessarily the complete output of every check.

### Exit codes

| Code | Meaning |
|---|---|
| `0` | Comparison passed |
| `1` | A regression exceeded configured thresholds |
| `2` | Input or execution error |

These codes allow CI jobs to pass or fail based on spatial-data quality checks.

## GitHub Actions

This repository's [CI workflow](.github/workflows/ci.yml) runs tests on **Python 3.11, 3.12, and 3.13**, on pushes and pull requests targeting `main`.

To use GeoDiff in another GitHub Actions job, install it first, then run a comparison. For example, after checking out the relevant repository and making the datasets available:

```yaml
- name: Install GeoDiff
  run: python -m pip install -e .

- name: Check geospatial regressions
  run: >
    geodiff compare
    data/baseline.geojson
    data/candidate.geojson
    --max-feature-loss 2
    --min-bbox-coverage 95
```

> The example assumes the job is running inside a checkout containing the GeoDiff package. If your workflow is in another repository, install GeoDiff from its GitHub source or another supported distribution mechanism, and adjust the dataset paths.

## Development

Install development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the tests:

```bash
pytest -v
```

The test suite covers feature counts, thresholds, schema/CRS changes, geometry types, null and invalid geometries, bounding-box coverage, and JSON reports.

### Project structure

```text
geodiff-ci/
├── .github/workflows/ci.yml
├── examples/
│   ├── baseline.geojson
│   └── candidate.geojson
├── src/geodiff/
│   ├── __init__.py
│   ├── cli.py
│   ├── compare.py
│   ├── report.py
│   └── spatial.py
├── tests/
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## Design principles

- Explicit regression rules and configurable tolerances
- Deterministic comparisons and geospatial-aware checks
- Machine-readable output and useful process exit codes
- Testable functions with minimal infrastructure requirements

GeoDiff is intentionally a focused **developer tool**, rather than a dashboard or visualization platform.

## Roadmap

Possible future improvements include:

- Duplicate feature ID detection
- Geometry area and length drift
- Attribute type and numeric distribution changes
- Configuration-file-based thresholds
- Markdown CI reports
- Per-check enable/disable controls
- Additional geospatial formats

These are **ideas**, not features already implemented.

## Technology

Python · GeoPandas · Shapely · PyArrow · Typer · Rich · Pytest · GitHub Actions

## License

MIT License. See [LICENSE](LICENSE).
