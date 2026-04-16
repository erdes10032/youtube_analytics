from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from youtube_analytics.models import VideoMetrics


@dataclass(frozen=True, slots=True)
class ReportRow:
    """A normalized row rendered in the output report."""

    title: str
    ctr: float
    retention_rate: float


class Report(ABC):
    """Base contract for all report implementations."""

    name: str

    @abstractmethod
    def build(self, videos: list[VideoMetrics]) -> list[ReportRow]:
        """Build report rows from source video metrics."""
