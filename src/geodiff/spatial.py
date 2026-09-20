import math


def _get_bounds(gdf):
    """Return finite dataset bounds or None."""

    if gdf.empty:
        return None

    if gdf.geometry.dropna().empty:
        return None

    bounds = gdf.total_bounds

    if not all(
        math.isfinite(value)
        for value in bounds
    ):
        return None

    return tuple(
        float(value)
        for value in bounds
    )


def _axis_coverage(
    baseline_min,
    baseline_max,
    candidate_min,
    candidate_max,
):
    """Calculate candidate coverage along one baseline axis."""

    baseline_span = (
        baseline_max - baseline_min
    )

    if baseline_span == 0:
        if (
            candidate_min
            <= baseline_min
            <= candidate_max
        ):
            return 1.0

        return 0.0

    overlap = max(
        0.0,
        min(
            baseline_max,
            candidate_max,
        )
        - max(
            baseline_min,
            candidate_min,
        ),
    )

    return min(
        overlap / baseline_span,
        1.0,
    )


def compare_spatial_extent(
    baseline,
    candidate,
    min_coverage_percent: float = 0.0,
):
    """
    Compare candidate bounding-box coverage
    against the baseline bounding box.
    """

    if not (
        0.0
        <= min_coverage_percent
        <= 100.0
    ):
        raise ValueError(
            "Minimum bounding-box coverage "
            "must be between 0 and 100."
        )

    baseline_bounds = _get_bounds(
        baseline
    )

    candidate_bounds = _get_bounds(
        candidate
    )

    if baseline_bounds is None:
        coverage_percent = 100.0

    elif candidate_bounds is None:
        coverage_percent = 0.0

    else:
        (
            baseline_min_x,
            baseline_min_y,
            baseline_max_x,
            baseline_max_y,
        ) = baseline_bounds

        (
            candidate_min_x,
            candidate_min_y,
            candidate_max_x,
            candidate_max_y,
        ) = candidate_bounds

        x_coverage = _axis_coverage(
            baseline_min_x,
            baseline_max_x,
            candidate_min_x,
            candidate_max_x,
        )

        y_coverage = _axis_coverage(
            baseline_min_y,
            baseline_max_y,
            candidate_min_y,
            candidate_max_y,
        )

        coverage_percent = (
            x_coverage
            * y_coverage
            * 100.0
        )

    coverage_percent = round(
        coverage_percent,
        2,
    )

    return {
        "baseline": (
            list(baseline_bounds)
            if baseline_bounds
            is not None
            else None
        ),
        "candidate": (
            list(candidate_bounds)
            if candidate_bounds
            is not None
            else None
        ),
        "coverage_percent": (
            coverage_percent
        ),
        "required_coverage_percent": (
            min_coverage_percent
        ),
        "passed": (
            coverage_percent
            >= min_coverage_percent
        ),
    }