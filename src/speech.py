from pathlib import Path
from typing import cast

import pyttsx3


def export_audio(*, text: str, export_filepath: Path) -> None:
    """Exports the given text to an mp3 audio file at the given path."""
    engine = cast(pyttsx3.Engine, pyttsx3.init())  # pyright: ignore reportUnknownVariableType
    engine.setProperty("rate", 110)  # pyright: ignore reportUnknownVariableType
    engine.setProperty("volume", 0.8)  # pyright: ignore reportUnknownVariableType
    engine.save_to_file(text, str(export_filepath))  # pyright: ignore reportUnknownVariableType
    engine.runAndWait()
