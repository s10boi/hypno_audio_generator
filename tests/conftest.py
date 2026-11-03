lazy from collections.abc import Callable

import pytest

type FeedInput = Callable[..., None]


@pytest.fixture
def feed_input(monkeypatch: pytest.MonkeyPatch) -> FeedInput:
    """Returns a function that makes `input()` return the given responses, in order."""

    def feed(*responses: str) -> None:
        answers = iter(responses)
        monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))

    return feed
