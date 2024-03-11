from collections.abc import Sequence
from random import shuffle


def ordered_lines(lines: Sequence[str]) -> list[str]:
    return list(lines)


def shuffle_lines(lines: Sequence[str]) -> list[str]:
    shuffled_lines = list(lines)
    shuffle(shuffled_lines)
    return shuffled_lines
