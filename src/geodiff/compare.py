from pathlib import Path

import geopandas as gpd


def load_geodata(path: str):
    """Load a supported geospatial dataset."""

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    suffix = file_path.suffix.lower()

    if suffix == ".parquet":
        return gpd.read_parquet(file_path)

    if suffix in {
        ".geojson",
        ".json",
        ".gpkg",
        ".shp",
    }:
        return gpd.read_file(file_path)

    raise ValueError(
        f"Unsupported file format: {suffix}"
    )


def compare_feature_count(
    baseline,
    candidate,
    max_loss_percent: float = 0.0,
):
    """Compare feature counts with an allowed loss percentage."""

    baseline_count = len(baseline)
    candidate_count = len(candidate)

    difference = (
        candidate_count - baseline_count
    )

    features_lost = max(
        baseline_count - candidate_count,
        0,
    )

    if baseline_count == 0:
        loss_percent = 0.0
    else:
        loss_percent = (
            features_lost
            / baseline_count
            * 100
        )

    return {
        "baseline": baseline_count,
        "candidate": candidate_count,
        "difference": difference,
        "loss_percent": round(
            loss_percent,
            2,
        ),
        "allowed_loss_percent": (
            max_loss_percent
        ),
        "passed": (
            loss_percent
            <= max_loss_percent
        ),
    }


def compare_schema(
    baseline,
    candidate,
):
    """Compare dataset columns."""

    baseline_columns = set(
        baseline.columns
    )

    candidate_columns = set(
        candidate.columns
    )

    added = sorted(
        candidate_columns
        - baseline_columns
    )

    removed = sorted(
        baseline_columns
        - candidate_columns
    )

    return {
        "added": added,
        "removed": removed,
        "passed": len(removed) == 0,
    }


def compare_crs(
    baseline,
    candidate,
):
    """Compare coordinate reference systems."""

    baseline_crs = str(
        baseline.crs
    )

    candidate_crs = str(
        candidate.crs
    )

    return {
        "baseline": baseline_crs,
        "candidate": candidate_crs,
        "passed": (
            baseline.crs
            == candidate.crs
        ),
    }


def compare_geometry_types(
    baseline,
    candidate,
):
    """Compare geometry types."""

    baseline_types = sorted(
        baseline.geometry
        .geom_type
        .dropna()
        .unique()
        .tolist()
    )

    candidate_types = sorted(
        candidate.geometry
        .geom_type
        .dropna()
        .unique()
        .tolist()
    )

    return {
        "baseline": baseline_types,
        "candidate": candidate_types,
        "passed": (
            baseline_types
            == candidate_types
        ),
    }


def compare_null_geometries(
    baseline,
    candidate,
    max_increase: int = 0,
):
    """Compare missing geometry counts."""

    baseline_nulls = int(
        baseline.geometry
        .isna()
        .sum()
    )

    candidate_nulls = int(
        candidate.geometry
        .isna()
        .sum()
    )

    increase = max(
        candidate_nulls
        - baseline_nulls,
        0,
    )

    return {
        "baseline": baseline_nulls,
        "candidate": candidate_nulls,
        "difference": (
            candidate_nulls
            - baseline_nulls
        ),
        "allowed_increase": max_increase,
        "passed": (
            increase <= max_increase
        ),
    }


def compare_invalid_geometries(
    baseline,
    candidate,
    max_increase: int = 0,
):
    """Compare invalid geometry counts."""

    baseline_invalid = int(
        (
            ~baseline.geometry.is_valid
            & baseline.geometry.notna()
        ).sum()
    )

    candidate_invalid = int(
        (
            ~candidate.geometry.is_valid
            & candidate.geometry.notna()
        ).sum()
    )

    increase = max(
        candidate_invalid
        - baseline_invalid,
        0,
    )

    return {
        "baseline": baseline_invalid,
        "candidate": candidate_invalid,
        "difference": (
            candidate_invalid
            - baseline_invalid
        ),
        "allowed_increase": max_increase,
        "passed": (
            increase <= max_increase
        ),
    }


def compare_datasets(
    baseline_path: str,
    candidate_path: str,
    max_feature_loss: float = 0.0,
    max_null_increase: int = 0,
    max_invalid_increase: int = 0,
):
    """Run all GeoDiff regression checks."""

    baseline = load_geodata(
        baseline_path
    )

    candidate = load_geodata(
        candidate_path
    )

    results = {
        "feature_count": (
            compare_feature_count(
                baseline,
                candidate,
                max_loss_percent=(
                    max_feature_loss
                ),
            )
        ),
        "schema": compare_schema(
            baseline,
            candidate,
        ),
        "crs": compare_crs(
            baseline,
            candidate,
        ),
        "geometry_types": (
            compare_geometry_types(
                baseline,
                candidate,
            )
        ),
        "null_geometries": (
            compare_null_geometries(
                baseline,
                candidate,
                max_increase=(
                    max_null_increase
                ),
            )
        ),
        "invalid_geometries": (
            compare_invalid_geometries(
                baseline,
                candidate,
                max_increase=(
                    max_invalid_increase
                ),
            )
        ),
    }

    results["passed"] = all(
        check["passed"]
        for check in results.values()
        if isinstance(check, dict)
        and "passed" in check
    )

    return results