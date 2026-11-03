# pyright: reportPrivateUsage=false

from functools import partial
lazy from pathlib import Path

from src.text_processing.get_text import _process_file
from src.text_processing.line_providers import ordered_lines
from src.text_processing.progress_providers import get_progress_marker_cycle_nums


def test_process_file_speaks_progress_markers_after_completed_cycles(tmp_path: Path) -> None:
    filepath = tmp_path / "lines.txt"
    _ = filepath.write_text("A\nB\n", encoding="utf-8")

    lines = _process_file(
        filepath=filepath,
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
