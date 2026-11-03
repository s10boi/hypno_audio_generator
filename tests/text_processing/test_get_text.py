# pyright: reportPrivateUsage=false

from functools import partial
lazy from pathlib import Path

from src.text_processing.get_text import _process_lines, _read_lines
from src.text_processing.line_providers import ordered_lines
from src.text_processing.progress_providers import get_progress_marker_cycle_nums


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
