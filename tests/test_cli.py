from pathlib import Path

from youtube_analytics.cli import main

CSV_HEADER = "title,ctr,retention_rate,views,likes,avg_watch_time\n"


def write_csv(path: Path, rows: list[str]) -> None:
    path.write_text(CSV_HEADER + "".join(rows), encoding="utf-8")


def test_cli_prints_clickbait_report_for_multiple_files(
    tmp_path: Path,
    capsys,
) -> None:
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
            "Video D,16.0,39,100,10,2.0\n",
        ],
    )

    exit_code = main(
        [
            "--files",
            str(first_file),
            str(second_file),
            "--report",
            "clickbait",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Video C" in captured.out
    assert "Video A" in captured.out
    assert "Video D" in captured.out
    assert "Video B" not in captured.out
    assert captured.out.index("Video C") < captured.out.index("Video A")


def test_cli_returns_error_for_unknown_report(tmp_path: Path, capsys) -> None:
    csv_file = tmp_path / "stats.csv"
    write_csv(csv_file, ["Video A,18.2,35,100,10,4.2\n"])

    exit_code = main(["--files", str(csv_file), "--report", "unknown"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Unknown report: unknown" in captured.err


def test_cli_returns_error_for_missing_file(capsys) -> None:
    exit_code = main(["--files", "missing.csv", "--report", "clickbait"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Input file does not exist" in captured.err
