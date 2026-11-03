from random import shuffle
lazy from collections.abc import Sequence


def ordered_lines(lines: Sequence[str]) -> list[str]:
    return list(lines)


def shuffle_lines(lines: Sequence[str]) -> list[str]:
    shuffled_lines = list(lines)
    shuffle(shuffled_lines)
    return shuffled_lines
