from functools import partial
lazy from collections.abc import Callable, Sequence
lazy from pathlib import Path

from src.text_processing.line_providers import ordered_lines, shuffle_lines
from src.text_processing.progress_providers import get_no_progress_markers, get_progress_marker_cycle_nums
from src.ux import get_bool_user_choice, get_int_user_choice_ge, get_user_choice_from_sequence

type LineProviderFunc = Callable[[Sequence[str]], list[str]]
type ProgressProviderFunc = Callable[[], dict[int, int]]


class NoTextFilesError(Exception):
    """Raised when the import directory contains no text files."""

    def __init__(self, import_dir: Path) -> None:
        """Initialises the error.

        Args:
            import_dir (Path): The directory that was searched for text files.
        """
        super().__init__(f"No text files found in {import_dir}")
        self.import_dir = import_dir


def _read_lines(filepath: Path) -> list[str]:
    """Reads the lines of a UTF-8 text file, skipping blank lines and removing trailing full stops.

    A UTF-8 byte order mark at the start of the file (as added by some Windows editors) is ignored.

    Args:
        filepath (Path): The filepath to the file to read.

    Returns:
        list[str]: The non-blank lines of the file.
    """
    text = filepath.read_text(encoding="utf-8-sig")
    return [stripped for line in text.splitlines() if (stripped := line.strip().removesuffix("."))]


def _process_lines(
    *,
    lines: Sequence[str],
    num_cycles: int,
    line_provider: LineProviderFunc,
    progress_provider: ProgressProviderFunc,
) -> list[str]:
    """Generates text from lines, using the given `line_provider` and `progress_provider` functions.

    Args:
        lines (Sequence[str]): The lines to repeat.
        num_cycles (int): The number of times to repeat the lines.
        line_provider (LineProviderFunc): The function to use to generate the lines.
        progress_provider (ProgressProviderFunc): The function to use to generate the progress markers.

    Returns:
        list[str]: The generated text as a list of strings.
    """
    final_lines: list[str] = []

    # Getting progress marker cycle nums, if any
    progress_report_cycles = progress_provider()

    # repeat the lines num_cycles times
    for completed_cycles in range(1, num_cycles + 1):
        generated_lines = line_provider(lines)
        final_lines.extend(generated_lines)

        if completed_cycles in progress_report_cycles:
            final_lines.append(f"Programming at {progress_report_cycles[completed_cycles]} percent")

    return final_lines


def _get_text_from_lines(*, lines: Sequence[str]) -> list[str]:
    """Generates text from the lines of a file chosen by the user.

    The user is prompted to choose options for the file, including the number of times to repeat it, whether to shuffle
    the lines, and whether to add progress markers. The text is generated and returned as a list of strings.

    Args:
        lines (Sequence[str]): The lines read from the chosen file.

    Returns:
        list[str]: The generated text as a list of strings.
    """
    num_cycles = get_int_user_choice_ge(
        message=(
            "\nEnter the number of times (cycles) to repeat this file\n"
            "- ALL lines from this file will be used in each cycle.\n"
            "- Must be 1 or higher."
        ),
        min_value=1,
    )

    if get_bool_user_choice(
        message=(
            "\nShuffle line order?\n"
            "- If 'yes', the lines will be shuffled before being repeated and will be in a different order each cycle\n"
            "- If 'no', the lines will be repeated in the order specified in the input file."
        ),
    ):
        line_provider = shuffle_lines
    else:
        line_provider = ordered_lines

    if num_cycles > 1 and (
        get_bool_user_choice(
            message=(
                "\nAdd audible progress reports?\n"
                "- If 'yes', progress markers will be added to the text at regular intervals (specified in the next "
                "step). Progress reports will be spoken in between complete cycles, for example: 'Programming at 25%'\n"
                "- If 'no', no progress markers will be added."
            ),
        )
    ):
        num_markers = get_int_user_choice_ge(
            message=(
                "\nEnter the number of progress markers\n"
                "- For example, if you enter 4, progress markers will be added after 25%, 50% and 75% of the total "
                "cycles (the end of the file is 100%).\n"
                "- Must be 2 or higher."
            ),
            min_value=2,
        )
        progress_report_cycles = partial(get_progress_marker_cycle_nums, num_cycles=num_cycles, num_markers=num_markers)
    else:
        progress_report_cycles = get_no_progress_markers

    return _process_lines(
        lines=lines,
        num_cycles=num_cycles,
        line_provider=line_provider,
        progress_provider=progress_report_cycles,
    )


def get_text_from_files(*, import_dir: Path) -> str:
    """Generates text from files chosen by the user from `import_dir`.

    The user is prompted to choose a text file from `import_dir` and the number of times to repeat it, whether to
    shuffle the lines, and whether to add progress markers. The user can repeat this process as many times as they
    want, and the text from each file will be added to the final text. The final text is returned as a string.

    Args:
        import_dir (Path): The directory to import text files from.

    Returns:
        str: The final text, as a string.

    Raises:
        NoTextFilesError: If `import_dir` contains no text files.
    """
    text_filepaths = sorted(import_dir.glob("*.txt"))
    if not text_filepaths:
        raise NoTextFilesError(import_dir)

    final_text: list[str] = []

    if add_intro_outro := get_bool_user_choice(
        message=(
            "\nAdd intro and outro?\n"
            "- If 'yes', the program will start with the line 'Beginning program.' and end with the line 'Program "
            "complete.'\n"
            "- If 'no', the program will start and end with the text from the imported files."
        ),
    ):
        final_text.append("Beginning program")

    print(f"{'LOAD FILES':=^80}")

    while True:
        text_filepath = get_user_choice_from_sequence(
            text_filepaths,
            "\nEnter the number of the text file to import",
        )
        try:
            lines = _read_lines(text_filepath)
        except UnicodeDecodeError:
            print(f"\n{text_filepath.name} is not UTF-8 encoded. Re-save it as UTF-8 and choose it again.")
            continue
        if not lines:
            print(f"\n{text_filepath.name} has no lines in it. Choose another file.")
            continue

        file_text = _get_text_from_lines(lines=lines)
        final_text.extend(file_text)

        if not get_bool_user_choice("\nAdd another file?"):
            break

    if add_intro_outro:
        final_text.append("Program complete")

    return ". ".join(final_text)
