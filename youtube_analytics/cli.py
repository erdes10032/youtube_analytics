from __future__ import annotations

import argparse
import sys

from tabulate import tabulate

from youtube_analytics.loader import load_video_metrics
from youtube_analytics.reports.registry import (
    UnknownReportError,
    create_report_registry,
)


def configure_console_output() -> None:
    """Prefer UTF-8 console output when the runtime supports reconfiguration."""

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build reports from YouTube CSV analytics files."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="One or more CSV files with YouTube video metrics.",
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Report name to build. Example: clickbait.",
    )
    return parser


def render_table(rows: list[tuple[str, float, float]]) -> str:
    return tabulate(
        rows,
        headers=["title", "ctr", "retention_rate"],
        tablefmt="grid",
    )


def main(argv: list[str] | None = None) -> int:
    configure_console_output()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        videos = load_video_metrics(args.files)
        registry = create_report_registry()
        report = registry.get(args.report)
        rows = report.build(videos)
    except (FileNotFoundError, UnknownReportError) as error:
        print(str(error), file=sys.stderr)
        return 1

    printable_rows = [(row.title, row.ctr, row.retention_rate) for row in rows]
    print(render_table(printable_rows))
    return 0
