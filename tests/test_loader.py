from pathlib import Path

import pytest

from youtube_analytics.loader import load_video_metrics

CSV_HEADER = "title,ctr,retention_rate,views,likes,avg_watch_time\n"


def write_csv(path: Path, rows: list[str]) -> None:
    path.write_text(CSV_HEADER + "".join(rows), encoding="utf-8")


def test_load_video_metrics_merges_rows_from_multiple_files(tmp_path: Path) -> None:
    first_file = tmp_path / "stats1.csv"
    second_file = tmp_path / "stats2.csv"

    write_csv(
        first_file,
        [
            "Video A,18.2,35,100,10,4.2\n",
            "Video B,9.5,82,200,20,8.9\n",
        ],
    )
    write_csv(
        second_file,
        [
            "Video C,22.5,28,300,30,3.1\n",
        ],
    )

    videos = load_video_metrics([str(first_file), str(second_file)])

    assert [video.title for video in videos] == ["Video A", "Video B", "Video C"]
    assert videos[0].ctr == 18.2
    assert videos[2].retention_rate == 28


def test_load_video_metrics_raises_for_missing_file(tmp_path: Path) -> None:
    missing_file = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError, match="Input file does not exist"):
        load_video_metrics([str(missing_file)])
