import pytest

from src.ux import get_user_choice_from_sequence
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
