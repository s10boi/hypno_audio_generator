from src.files_io import get_import_export_dirs
from src.speech import export_audio
from src.text_processing.get_text import get_text_from_files


def main() -> None:
    import_dir, export_dir = get_import_export_dirs()

    try:
        text = get_text_from_files(import_dir=import_dir)
    except ValueError:
        print("No text files found in import directory. Exiting program.")
    else:
        output_filename = input("Enter output filename (without extension): ")
        export_filepath = export_dir / f"{output_filename}.wav"

        export_audio(text=text, export_filepath=export_filepath)


if __name__ == "__main__":
    main()
