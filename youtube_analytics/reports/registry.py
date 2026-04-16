from __future__ import annotations

from youtube_analytics.reports.base import Report
from youtube_analytics.reports.clickbait import ClickbaitReport


class UnknownReportError(ValueError):
    """Raised when user requests a report that is not registered."""


class ReportRegistry:
    """Stores available reports and returns them by name."""

    def __init__(self) -> None:
        self._reports: dict[str, Report] = {}

    def register(self, report: Report) -> None:
        self._reports[report.name] = report

    def get(self, report_name: str) -> Report:
        try:
            return self._reports[report_name]
        except KeyError as error:
            supported_reports = ", ".join(sorted(self._reports))
            raise UnknownReportError(
                f"Unknown report: {report_name}. Supported reports: {supported_reports}"
            ) from error


def create_report_registry() -> ReportRegistry:
    registry = ReportRegistry()
    registry.register(ClickbaitReport())
    return registry
