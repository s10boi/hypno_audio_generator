# pyright: reportPrivateUsage=false

lazy from pathlib import Path

from main import _get_export_filepath
lazy from tests.conftest import FeedInput


def test_get_export_filepath_adds_wav_extension(tmp_path: Path, feed_input: FeedInput) -> None:
    feed_input("session")

    assert _get_export_filepath(tmp_path) == tmp_path / "session.wav"


def test_get_export_filepath_overwrites_existing_file_when_confirmed(tmp_path: Path, feed_input: FeedInput) -> None:
    _ = (tmp_path / "session.wav").write_bytes(b"")
    feed_input("session", "y")

    assert _get_export_filepath(tmp_path) == tmp_path / "session.wav"


def test_get_export_filepath_asks_again_when_overwrite_declined(tmp_path: Path, feed_input: FeedInput) -> None:
    _ = (tmp_path / "session.wav").write_bytes(b"")
    feed_input("session", "n", "session 2")

    assert _get_export_filepath(tmp_path) == tmp_path / "session 2.wav"
