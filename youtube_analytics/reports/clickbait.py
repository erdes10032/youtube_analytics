from __future__ import annotations

from youtube_analytics.models import VideoMetrics
from youtube_analytics.reports.base import Report, ReportRow


class ClickbaitReport(Report):
    """Select videos with suspiciously high CTR and weak retention."""

    name = "clickbait"

    def build(self, videos: list[VideoMetrics]) -> list[ReportRow]:
        filtered_rows = [
            ReportRow(
                title=video.title,
                ctr=video.ctr,
                retention_rate=video.retention_rate,
            )
            for video in videos
            if video.ctr > 15 and video.retention_rate < 40
        ]
        return sorted(filtered_rows, key=lambda row: row.ctr, reverse=True)
