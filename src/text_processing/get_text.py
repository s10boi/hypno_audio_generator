from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING

from src.text_processing.line_providers import ordered_lines, shuffle_lines
from src.text_processing.progress_providers import get_no_progress_markers, get_progress_marker_cycle_nums
from src.ux import get_bool_user_choice, get_int_user_choice_ge, get_user_choice_from_sequence

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

type LineProviderFunc = Callable[[Sequence[str]], list[str]]
type ProgressProviderFunc = Callable[[], dict[int, int]]


def _process_file(
    *, filepath: Path, num_cycles: int, line_provider: LineProviderFunc, progress_provider: ProgressProviderFunc
) -> list[str]:
    """Generates text from a file, using the given `line_provider` and `progress_provider` functions.

    Args:
        filepath (Path): The filepath to the file to import.
        num_cycles (int): The number of times to repeat the file.
        line_provider (LineProviderFunc): The function to use to generate the lines.
        progress_provider (ProgressProviderFunc): The function to use to generate the progress markers.

    Returns:
        list[str]: The generated text as a list of strings.
    """
    final_lines: list[str] = []

    # Getting progress marker cycle nums, if any
    progress_report_cycles = progress_provider()

    # open the filepath and make a list of each line
    with filepath.open() as file:
        lines = [line.replace("\n", "").strip().removesuffix(".") for line in file.readlines()]

    # repeat the lines num_cycles times
    for cycle in range(num_cycles):
        generated_lines = line_provider(lines)
        final_lines.extend(generated_lines)

        if cycle in progress_report_cycles:
            final_lines.append(f"Programming at {progress_report_cycles[cycle]} percent")

    return final_lines


def _get_text_from_file(*, import_filepath: Path) -> list[str]:
    """Generates text from a file chosen by the user.

    The user is prompted to choose options for the file, including the number of times to repeat it, whether to shuffle
    the lines, and whether to add progress markers. The text is generated and returned as a list of strings.

    Args:
        import_filepath (Path): The filepath to the file to import.

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
        )
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
            )
        )
    ):
        num_markers = get_int_user_choice_ge(
            message=(
                "\nEnter the number of progress markers\n"
                "- For example, if you enter 4, progress markers will be added at 25%, 50%, 75%, and 100% of the "
                "total cycles.\n"
                "- Must be 2 or higher."
            ),
            min_value=2,
        )
        progress_report_cycles = partial(get_progress_marker_cycle_nums, num_cycles=num_cycles, num_markers=num_markers)
    else:
        progress_report_cycles = get_no_progress_markers

    return _process_file(
        filepath=import_filepath,
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
    """
    final_text: list[str] = []

    if add_intro_outro := get_bool_user_choice(
        message=(
            "\nAdd intro and outro?\n"
            "- If 'yes', the program will start with the line 'Begiining program.' and end with the line 'Program "
            "complete.'\n"
            "- If 'no', the program will start and end with the text from the imported files."
        )
    ):
        final_text.append("Beginning program.")

    print(f"{'LOAD FILES':=^80}")

    text_filepaths = sorted(import_dir.glob("*.txt"))

    while True:
        try:
            text_filepath = get_user_choice_from_sequence(
                text_filepaths, "\nEnter the number of the text file to import"
            )
        except ValueError as e:
            raise ValueError from e
        file_text = _get_text_from_file(import_filepath=text_filepath)
        final_text.extend(file_text)

        if not get_bool_user_choice("\nAdd another file?"):
            break

    if add_intro_outro:
        final_text.append("Program complete")

    return ". ".join(final_text)
