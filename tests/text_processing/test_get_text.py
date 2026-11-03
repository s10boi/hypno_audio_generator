# pyright: reportPrivateUsage=false

from functools import partial
lazy from pathlib import Path

import pytest

from src.text_processing.get_text import NoTextFilesError, _process_lines, _read_lines, get_text_from_files
from src.text_processing.line_providers import ordered_lines
from src.text_processing.progress_providers import get_progress_marker_cycle_nums
lazy from tests.conftest import FeedInput


def test_read_lines_strips_whitespace_and_trailing_full_stops(tmp_path: Path) -> None:
    filepath = tmp_path / "lines.txt"
    _ = filepath.write_text("  You are relaxed.  \nDeeper and deeper\n", encoding="utf-8")

    assert _read_lines(filepath) == ["You are relaxed", "Deeper and deeper"]


def test_read_lines_skips_blank_lines(tmp_path: Path) -> None:
    filepath = tmp_path / "lines.txt"
    _ = filepath.write_text("\nA\n\n   \n.\nB\n\n", encoding="utf-8")

    assert _read_lines(filepath) == ["A", "B"]


def test_read_lines_ignores_byte_order_mark(tmp_path: Path) -> None:
    filepath = tmp_path / "lines.txt"
    _ = filepath.write_text("A\nB\n", encoding="utf-8-sig")

    assert _read_lines(filepath) == ["A", "B"]


def test_read_lines_handles_windows_line_endings(tmp_path: Path) -> None:
    filepath = tmp_path / "lines.txt"
    _ = filepath.write_bytes(b"A.\r\nB\r\n")

    assert _read_lines(filepath) == ["A", "B"]


def test_process_lines_speaks_progress_markers_after_completed_cycles() -> None:
    lines = _process_lines(
        lines=["A", "B"],
        num_cycles=4,
        line_provider=ordered_lines,
        progress_provider=partial(get_progress_marker_cycle_nums, num_cycles=4, num_markers=4),
    )

    assert lines == [
        "A",
        "B",
        "Programming at 25 percent",
        "A",
        "B",
        "Programming at 50 percent",
        "A",
        "B",
        "Programming at 75 percent",
        "A",
        "B",
    ]


def test_get_text_from_files_raises_when_no_text_files(tmp_path: Path) -> None:
    _ = (tmp_path / "notes.md").write_text("Not a text file", encoding="utf-8")

    with pytest.raises(NoTextFilesError, match="No text files found"):
        _ = get_text_from_files(import_dir=tmp_path)


def test_get_text_from_files_reprompts_for_unreadable_and_empty_files(
    tmp_path: Path, feed_input: FeedInput, capsys: pytest.CaptureFixture[str]
) -> None:
    _ = (tmp_path / "a_latin1.txt").write_bytes(b"caf\xe9\n")
    _ = (tmp_path / "b_empty.txt").write_text("\n\n", encoding="utf-8")
    _ = (tmp_path / "c_good.txt").write_text("A\nB\n", encoding="utf-8")
    # intro/outro: no, file 1 (unreadable), file 2 (empty), file 3, 1 cycle, no shuffle, no more files
    feed_input("n", "1", "2", "3", "1", "n", "n")

    assert get_text_from_files(import_dir=tmp_path) == "A. B"
    output = capsys.readouterr().out
    assert "a_latin1.txt is not UTF-8 encoded" in output
    assert "b_empty.txt has no lines in it" in output
