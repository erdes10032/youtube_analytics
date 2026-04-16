from youtube_analytics.models import VideoMetrics
from youtube_analytics.reports.clickbait import ClickbaitReport
from youtube_analytics.reports.registry import (
    UnknownReportError,
    create_report_registry,
)


def test_clickbait_report_filters_and_sorts_rows() -> None:
    report = ClickbaitReport()
    videos = [
        VideoMetrics("Low CTR", 10.0, 20.0, 100, 10, 2.0),
        VideoMetrics("Too High Retention", 18.0, 45.0, 100, 10, 2.0),
        VideoMetrics("Second", 21.0, 35.0, 100, 10, 2.0),
        VideoMetrics("First", 25.0, 22.0, 100, 10, 2.0),
    ]

    rows = report.build(videos)

    assert [row.title for row in rows] == ["First", "Second"]
    assert [row.ctr for row in rows] == [25.0, 21.0]


def test_report_registry_returns_registered_report() -> None:
    registry = create_report_registry()

    report = registry.get("clickbait")

    assert isinstance(report, ClickbaitReport)


def test_report_registry_raises_for_unknown_report() -> None:
    registry = create_report_registry()

    try:
        registry.get("unknown")
    except UnknownReportError as error:
        assert "Supported reports: clickbait" in str(error)
    else:
        raise AssertionError("Expected UnknownReportError to be raised")
