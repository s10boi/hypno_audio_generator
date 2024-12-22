# pyright: reportPrivateUsage=false

import pytest

from src.text_processing.progress_providers import _get_percentages, get_progress_marker_cycle_nums


@pytest.mark.parametrize(
    argnames=("num_markers", "expected_output"),
    argvalues=[
        (2, [50]),
        (3, [33, 67]),
        (4, [25, 50, 75]),
        (5, [20, 40, 60, 80]),
        (10, [10, 20, 30, 40, 50, 60, 70, 80, 90]),
    ],
)
def test_get_percentages(num_markers: int, expected_output: list[int]) -> None:
    assert _get_percentages(num_markers=num_markers) == expected_output


@pytest.mark.parametrize(
    argnames=("num_cycles", "expected_output"),
    argvalues=[
        (2, {0: 20, 1: 60}),
        (3, {1: 40, 2: 80}),
        (4, {1: 20, 2: 60, 3: 80}),
        (5, {1: 20, 2: 40, 3: 60, 4: 80}),
        (10, {2: 20, 4: 40, 6: 60, 8: 80}),
        (17, {3: 20, 7: 40, 10: 60, 14: 80}),
    ],
)
def test_get_progress_marker_cycle_nums(num_cycles: int, expected_output: dict[int, int]) -> None:
    assert get_progress_marker_cycle_nums(num_cycles=num_cycles, num_markers=5) == expected_output


def test_get_progress_marker_cycle_nums_raises_value_error() -> None:
    with pytest.raises(ValueError):  # noqa: PT011
        _ = get_progress_marker_cycle_nums(num_cycles=1, num_markers=2)

    with pytest.raises(ValueError):  # noqa: PT011
        _ = get_progress_marker_cycle_nums(num_cycles=2, num_markers=1)
