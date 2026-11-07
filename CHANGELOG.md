# Changelog

All notable changes to GeoDiff CI are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses version numbers as declared in `pyproject.toml`.

## [Unreleased]

### Added

- `CHANGELOG.md` to track project changes.

## [0.1.0]

Initial version of GeoDiff CI.

### Added

- `geodiff` command-line interface built with Typer.
- `geodiff compare BASELINE CANDIDATE` command to compare a candidate geospatial dataset against a baseline.
- `geodiff version` command to show the current version.
- Regression checks for:
  - Feature count (added or removed features) and feature-loss percentage
  - Schema (added or removed columns)
  - Coordinate reference system (CRS) changes
  - Geometry type changes
  - Increase in null geometries
  - Increase in invalid geometries
  - Spatial extent (baseline bounding-box coverage by the candidate)
- Configurable thresholds:
  - `--max-feature-loss` (percentage, default `0`)
  - `--max-null-increase` (default `0`)
  - `--max-invalid-increase` (default `0`)
  - `--min-bbox-coverage` (percentage, default `0`, i.e. not enforced)
- Terminal regression report rendered with Rich.
- Machine-readable JSON report via `--json-output` / `-j`.
- CI-friendly exit codes: `0` (passed), `1` (regression exceeded thresholds), `2` (input or execution error).
- Support for input formats readable by GeoPandas, including GeoJSON, GeoParquet, GeoPackage and ESRI Shapefile.
- Example baseline and candidate GeoJSON datasets in `examples/`.
- Pytest test suite and GitHub Actions CI workflow running on Python 3.11, 3.12 and 3.13.
