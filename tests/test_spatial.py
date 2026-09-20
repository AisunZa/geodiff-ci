import geopandas as gpd

from shapely.geometry import (
    Point,
    box,
)

from geodiff.spatial import (
    compare_spatial_extent,
)


def make_gdf(
    geometry,
):
    return gpd.GeoDataFrame(
        {
            "geometry": [
                geometry
            ]
        },
        crs="EPSG:3857",
    )


def test_same_extent_has_full_coverage():

    baseline = make_gdf(
        box(
            0,
            0,
            10,
            10,
        )
    )

    candidate = make_gdf(
        box(
            0,
            0,
            10,
            10,
        )
    )

    result = (
        compare_spatial_extent(
            baseline,
            candidate,
            min_coverage_percent=100,
        )
    )

    assert (
        result[
            "coverage_percent"
        ]
        == 100.0
    )

    assert (
        result["passed"]
        is True
    )


def test_reduced_extent_is_detected():

    baseline = make_gdf(
        box(
            0,
            0,
            10,
            10,
        )
    )

    candidate = make_gdf(
        box(
            0,
            0,
            5,
            10,
        )
    )

    result = (
        compare_spatial_extent(
            baseline,
            candidate,
            min_coverage_percent=90,
        )
    )

    assert (
        result[
            "coverage_percent"
        ]
        == 50.0
    )

    assert (
        result["passed"]
        is False
    )


def test_larger_candidate_preserves_baseline_extent():

    baseline = make_gdf(
        box(
            0,
            0,
            10,
            10,
        )
    )

    candidate = make_gdf(
        box(
            -5,
            -5,
            15,
            15,
        )
    )

    result = (
        compare_spatial_extent(
            baseline,
            candidate,
            min_coverage_percent=100,
        )
    )

    assert (
        result[
            "coverage_percent"
        ]
        == 100.0
    )

    assert (
        result["passed"]
        is True
    )


def test_non_overlapping_extent_fails():

    baseline = make_gdf(
        box(
            0,
            0,
            10,
            10,
        )
    )

    candidate = make_gdf(
        box(
            20,
            20,
            30,
            30,
        )
    )

    result = (
        compare_spatial_extent(
            baseline,
            candidate,
            min_coverage_percent=1,
        )
    )

    assert (
        result[
            "coverage_percent"
        ]
        == 0.0
    )

    assert (
        result["passed"]
        is False
    )


def test_point_extent_is_supported():

    baseline = make_gdf(
        Point(
            5,
            5,
        )
    )

    candidate = make_gdf(
        Point(
            5,
            5,
        )
    )

    result = (
        compare_spatial_extent(
            baseline,
            candidate,
            min_coverage_percent=100,
        )
    )

    assert (
        result[
            "coverage_percent"
        ]
        == 100.0
    )

    assert (
        result["passed"]
        is True
    )