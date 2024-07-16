import sys
from pathlib import Path
from typing import cast

import pyttsx3


def get_engine() -> pyttsx3.Engine:
    """Overrides default pyttsx3 engine to fix issues with macOS TTS."""
    if sys.platform == "darwin":
        from src.speech.macos_override.engine import get_hypno_engine  # type: ignore # noqa: PLC0415

        engine = get_hypno_engine()
    else:
        engine = pyttsx3.init()  # type: ignore

    return engine


def export_audio(*, text: str, export_filepath: Path) -> None:
    """Exports the given text to an mp3 audio file at the given path."""
    engine = cast(pyttsx3.Engine, get_engine())  # pyright: ignore reportUnknownVariableType
    engine.setProperty("rate", 110)  # pyright: ignore reportUnknownVariableType
    engine.setProperty("volume", 0.8)  # pyright: ignore reportUnknownVariableType
    engine.save_to_file(text, str(export_filepath))  # pyright: ignore reportUnknownVariableType
    engine.runAndWait()
