lazy from pathlib import Path

from src.files_io import get_import_export_dirs
from src.speech import export_audio
from src.text_processing.get_text import NoTextFilesError, get_text_from_files
from src.ux import get_bool_user_choice, get_filename_user_choice


def _get_export_filepath(export_dir: Path) -> Path:
    """Asks the user for the output filename, confirming before an existing file is overwritten."""
    while True:
        output_filename = get_filename_user_choice("Enter output filename (without extension): ")
        export_filepath = export_dir / f"{output_filename}.wav"

        if not export_filepath.exists() or get_bool_user_choice(f"\n{export_filepath} already exists. Overwrite it?"):
            return export_filepath


def main() -> None:
    import_dir, export_dir = get_import_export_dirs()

    try:
        text = get_text_from_files(import_dir=import_dir)
    except NoTextFilesError as e:
        print(f"{e}. Add some .txt files and run the program again.")
    else:
        export_filepath = _get_export_filepath(export_dir)

        export_audio(text=text, export_filepath=export_filepath)


if __name__ == "__main__":
    main()
