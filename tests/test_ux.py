# pyright: reportPrivateUsage=false

import pytest

from src.ux import _get_filename_problem, get_filename_user_choice, get_user_choice_from_sequence
lazy from tests.conftest import FeedInput


def test_get_user_choice_from_sequence_returns_chosen_item(feed_input: FeedInput) -> None:
    feed_input("2")

    assert get_user_choice_from_sequence(["a", "b", "c"], "Choose") == "b"


def test_get_user_choice_from_sequence_reprompts_on_invalid_input(
    feed_input: FeedInput, capsys: pytest.CaptureFixture[str]
) -> None:
    invalid_inputs = ("abc", "", "0", "4")
    feed_input(*invalid_inputs, "3")

    assert get_user_choice_from_sequence(["a", "b", "c"], "Choose") == "c"
    assert capsys.readouterr().out.count("Invalid choice") == len(invalid_inputs)


def test_get_user_choice_from_sequence_raises_on_empty_sequence() -> None:
    with pytest.raises(ValueError, match="empty"):
        _ = get_user_choice_from_sequence([], "Choose")


@pytest.mark.parametrize("filename", ["session", "My Session 01", "deep-trance_v2", "café", "con1", "file.name"])
def test_get_filename_problem_accepts_valid_filenames(filename: str) -> None:
    assert _get_filename_problem(filename) is None


@pytest.mark.parametrize(
    argnames=("filename", "expected_problem"),
    argvalues=[
        ("", "can't be empty"),
        ("a/b", "can't contain '/'"),
        ("a\\b", "can't contain '\\\\'"),
        ("what?:", "can't contain ':' '?'"),
        ("tab\tname", "can't contain '\\t'"),
        ("ends.", "can't end with a full stop"),
        ("CON", "reserved filename on Windows"),
        ("nul", "reserved filename on Windows"),
        ("com1.backup", "reserved filename on Windows"),
    ],
)
def test_get_filename_problem_rejects_invalid_filenames(filename: str, expected_problem: str) -> None:
    problem = _get_filename_problem(filename)

    assert problem is not None
    assert expected_problem in problem


def test_get_filename_user_choice_reprompts_until_valid(
    feed_input: FeedInput, capsys: pytest.CaptureFixture[str]
) -> None:
    invalid_inputs = ("", "a/b")
    feed_input(*invalid_inputs, "  session  ")

    assert get_filename_user_choice("Filename: ") == "session"
    assert capsys.readouterr().out.count("Try again") == len(invalid_inputs)
