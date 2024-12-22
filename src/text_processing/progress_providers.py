def _get_percentages(num_markers: int) -> list[int]:
    return [round(marker * 100 / num_markers) for marker in range(1, num_markers)]


def get_progress_marker_cycle_nums(*, num_cycles: int, num_markers: int) -> dict[int, int]:
    """Return a dictionary of progress markers for the given `num_cycles`.

    Progress markers are evenly spaced throughout the cycles, and are spaced according to the number of markers
    specified by the user. The cycle number is the key, and the percentage is the value. The 100% marker is not included
    in the dictionary.

    Both `num_cycles` and `num_markers` must be greater than 1, as there is no point in adding progress markers if there
    is only one cycle, or if there is only one marker.

    Args:
        num_cycles (int): The number of cycles to repeat the text.
        num_markers (int): The number of progress markers to add.

    Returns:
        dict[int, int]: A dictionary of percentage and cycle number progress markers.

    Raises:
        ValueError: If `num_cycles` or `num_markers` is less than 2.

    Examples:
        >>> _get_progress_marker_cycle_nums(num_cycles=2, num_markers=2)
        {1: 50}
        >>> _get_progress_marker_cycle_nums(num_cycles=3, num_markers=2)
        {1: 33, 2: 67}
        >>> _get_progress_marker_cycle_nums(num_cycles=4, num_markers=2)
        {1: 25, 2: 50, 3: 75}
        >>> _get_progress_marker_cycle_nums(num_cycles=20, num_markers=5)
        {4: 20, 8: 40, 12: 60, 16: 80}
    """
    progress_markers: dict[int, int] = {}

    if num_markers < 2 or num_cycles < 2:  # noqa: PLR2004
        msg = "num_markers and num_cycles must be greater than 1"
        raise ValueError(msg)

    for percentage in _get_percentages(num_markers):
        percentage_index = round(num_cycles * (percentage / 100))
        if percentage_index != num_cycles:
            progress_markers[percentage_index] = percentage

    return progress_markers


def get_no_progress_markers() -> dict[int, int]:
    return {}
