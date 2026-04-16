from __future__ import annotations

import csv
from pathlib import Path

from youtube_analytics.models import VideoMetrics


def load_video_metrics(file_paths: list[str]) -> list[VideoMetrics]:
    """Load and merge video metrics from all provided CSV files."""

    rows: list[VideoMetrics] = []
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file does not exist: {path}")
        if not path.is_file():
            raise FileNotFoundError(f"Input path is not a file: {path}")

        with path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            for raw_row in reader:
                rows.append(
                    VideoMetrics(
                        title=raw_row["title"],
                        ctr=float(raw_row["ctr"]),
                        retention_rate=float(raw_row["retention_rate"]),
                        views=int(raw_row["views"]),
                        likes=int(raw_row["likes"]),
                        avg_watch_time=float(raw_row["avg_watch_time"]),
                    )
                )

    return rows
