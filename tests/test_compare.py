import geopandas as gpd

from shapely.geometry import (
    Point,
    Polygon,
)

from geodiff.compare import (
    compare_crs,
    compare_feature_count,
    compare_geometry_types,
    compare_invalid_geometries,
    compare_null_geometries,
    compare_schema,
)


def make_points(count):
    return gpd.GeoDataFrame(
        {
            "id": list(
                range(count)
            ),
            "geometry": [
                Point(i, i)
                for i in range(count)
            ],
        },
        crs="EPSG:4326",
    )


def test_feature_count_regression_detected():

    baseline = make_points(10)
    candidate = make_points(9)

    result = compare_feature_count(
        baseline,
        candidate,
    )

    assert result["difference"] == -1
    assert result["loss_percent"] == 10.0
    assert result["passed"] is False


def test_feature_loss_threshold_allows_change():

    baseline = make_points(10)
    candidate = make_points(9)

    result = compare_feature_count(
        baseline,
        candidate,
        max_loss_percent=10,
    )

    assert result["loss_percent"] == 10.0
    assert result["passed"] is True


def test_feature_loss_threshold_rejects_excessive_loss():

    baseline = make_points(10)
    candidate = make_points(8)

    result = compare_feature_count(
        baseline,
        candidate,
        max_loss_percent=10,
    )

    assert result["loss_percent"] == 20.0
    assert result["passed"] is False


def test_feature_count_passes_when_no_features_lost():

    baseline = make_points(1)
    candidate = make_points(2)

    result = compare_feature_count(
        baseline,
        candidate,
    )

    assert result["loss_percent"] == 0.0
    assert result["passed"] is True


def test_schema_regression_detected():

    baseline = gpd.GeoDataFrame(
        {
            "id": [1],
            "name": ["A"],
            "geometry": [
                Point(0, 0)
            ],
        }
    )

    candidate = gpd.GeoDataFrame(
        {
            "id": [1],
            "geometry": [
                Point(0, 0)
            ],
        }
    )

    result = compare_schema(
        baseline,
        candidate,
    )

    assert result["removed"] == [
        "name"
    ]

    assert result["passed"] is False


def test_added_column_is_allowed():

    baseline = gpd.GeoDataFrame(
        {
            "id": [1],
            "geometry": [
                Point(0, 0)
            ],
        }
    )

    candidate = gpd.GeoDataFrame(
        {
            "id": [1],
            "name": ["A"],
            "geometry": [
                Point(0, 0)
            ],
        }
    )

    result = compare_schema(
        baseline,
        candidate,
    )

    assert result["added"] == [
        "name"
    ]

    assert result["removed"] == []

    assert result["passed"] is True


def test_crs_match():

    baseline = gpd.GeoDataFrame(
        geometry=[
            Point(0, 0)
        ],
        crs="EPSG:4326",
    )

    candidate = gpd.GeoDataFrame(
        geometry=[
            Point(1, 1)
        ],
        crs="EPSG:4326",
    )

    result = compare_crs(
        baseline,
        candidate,
    )

    assert result["passed"] is True


def test_crs_regression_detected():

    baseline = gpd.GeoDataFrame(
        geometry=[
            Point(0, 0)
        ],
        crs="EPSG:4326",
    )

    candidate = gpd.GeoDataFrame(
        geometry=[
            Point(1, 1)
        ],
        crs="EPSG:3857",
    )

    result = compare_crs(
        baseline,
        candidate,
    )

    assert result["passed"] is False


def test_geometry_type_change_detected():

    baseline = gpd.GeoDataFrame(
        geometry=[
            Point(0, 0)
        ]
    )

    candidate = gpd.GeoDataFrame(
        geometry=[
            Polygon(
                [
                    (0, 0),
                    (0, 1),
                    (1, 1),
                    (1, 0),
                    (0, 0),
                ]
            )
        ]
    )

    result = compare_geometry_types(
        baseline,
        candidate,
    )

    assert result["passed"] is False


def test_null_geometry_regression_detected():

    baseline = gpd.GeoDataFrame(
        geometry=[
            Point(0, 0),
            Point(1, 1),
        ]
    )

    candidate = gpd.GeoDataFrame(
        geometry=[
            Point(0, 0),
            None,
        ]
    )

    result = compare_null_geometries(
        baseline,
        candidate,
    )

    assert result["candidate"] == 1
    assert result["passed"] is False


def test_null_geometry_threshold_allows_change():

    baseline = gpd.GeoDataFrame(
        geometry=[
            Point(0, 0),
            Point(1, 1),
        ]
    )

    candidate = gpd.GeoDataFrame(
        geometry=[
            Point(0, 0),
            None,
        ]
    )

    result = compare_null_geometries(
        baseline,
        candidate,
        max_increase=1,
    )

    assert result["passed"] is True


def test_invalid_geometry_regression_detected():

    valid_polygon = Polygon(
        [
            (0, 0),
            (0, 2),
            (2, 2),
            (2, 0),
            (0, 0),
        ]
    )

    invalid_polygon = Polygon(
        [
            (0, 0),
            (2, 2),
            (2, 0),
            (0, 2),
            (0, 0),
        ]
    )

    baseline = gpd.GeoDataFrame(
        geometry=[
            valid_polygon
        ]
    )

    candidate = gpd.GeoDataFrame(
        geometry=[
            invalid_polygon
        ]
    )

    result = compare_invalid_geometries(
        baseline,
        candidate,
    )

    assert result["candidate"] == 1
    assert result["passed"] is False


def test_invalid_geometry_threshold_allows_change():

    valid_polygon = Polygon(
        [
            (0, 0),
            (0, 2),
            (2, 2),
            (2, 0),
            (0, 0),
        ]
    )

    invalid_polygon = Polygon(
        [
            (0, 0),
            (2, 2),
            (2, 0),
            (0, 2),
            (0, 0),
        ]
    )

    baseline = gpd.GeoDataFrame(
        geometry=[
            valid_polygon
        ]
    )

    candidate = gpd.GeoDataFrame(
        geometry=[
            invalid_polygon
        ]
    )

    result = compare_invalid_geometries(
        baseline,
        candidate,
        max_increase=1,
    )

    assert result["passed"] is True