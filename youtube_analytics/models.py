from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VideoMetrics:
    """Represents one video row from the source CSV file."""

    title: str
    ctr: float
    retention_rate: float
    views: int
    likes: int
    avg_watch_time: float
