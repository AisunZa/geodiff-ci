import json

from geodiff.report import write_json_report


def test_write_json_report(tmp_path):

    results = {
        "feature_count": {
            "baseline": 10,
            "candidate": 8,
            "difference": -2,
            "passed": False,
        },
        "passed": False,
    }

    output = tmp_path / "report.json"

    returned_path = write_json_report(
        results,
        output,
    )

    assert returned_path == output
    assert output.exists()

    with output.open(
        "r",
        encoding="utf-8",
    ) as file:
        saved = json.load(file)

    assert saved == results
    assert saved["passed"] is False


def test_write_json_report_creates_directory(
    tmp_path,
):

    results = {
        "passed": True,
    }

    output = (
        tmp_path
        / "reports"
        / "geodiff.json"
    )

    write_json_report(
        results,
        output,
    )

    assert output.exists()