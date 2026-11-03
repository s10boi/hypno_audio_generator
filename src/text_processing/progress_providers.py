def _get_percentages(num_markers: int) -> list[int]:
    return [round(marker * 100 / num_markers) for marker in range(1, num_markers)]


def get_progress_marker_cycle_nums(*, num_cycles: int, num_markers: int) -> dict[int, int]:
    """Return a dictionary of progress markers for the given `num_cycles`.

    Progress markers are evenly spaced throughout the cycles, and are spaced according to the number of markers
    specified by the user. The key is the number of completed cycles after which the marker is spoken, and the value is
    the percentage. Markers that would fall before the first cycle or after the last cycle (100%) are not included. If
    two markers fall after the same cycle, the later percentage is used.

    Both `num_cycles` and `num_markers` must be greater than 1, as there is no point in adding progress markers if there
    is only one cycle, or if there is only one marker.

    Args:
        num_cycles (int): The number of cycles to repeat the text.
        num_markers (int): The number of progress markers to add.

    Returns:
        dict[int, int]: A dictionary of completed cycle counts to percentages.

    Raises:
        ValueError: If `num_cycles` or `num_markers` is less than 2.

    Examples:
        >>> get_progress_marker_cycle_nums(num_cycles=2, num_markers=2)
        {1: 50}
        >>> get_progress_marker_cycle_nums(num_cycles=4, num_markers=4)
        {1: 25, 2: 50, 3: 75}
        >>> get_progress_marker_cycle_nums(num_cycles=20, num_markers=5)
        {4: 20, 8: 40, 12: 60, 16: 80}
        >>> get_progress_marker_cycle_nums(num_cycles=300, num_markers=3)
        {100: 33, 200: 67}
    """
    progress_markers: dict[int, int] = {}

    if num_markers < 2 or num_cycles < 2:  # ruff: ignore[magic-value-comparison]
        msg = "num_markers and num_cycles must be greater than 1"
        raise ValueError(msg)

    for marker, percentage in enumerate(_get_percentages(num_markers), start=1):
        completed_cycles = round(num_cycles * marker / num_markers)
        if 0 < completed_cycles < num_cycles:
            progress_markers[completed_cycles] = percentage

    return progress_markers


def get_no_progress_markers() -> dict[int, int]:
    return {}
