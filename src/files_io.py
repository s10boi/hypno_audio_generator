from pathlib import Path


def get_import_export_dirs() -> tuple[Path, Path]:
    """Get import and export directories.

    Both directories are in the data directory and are created if they don't exist.

    Returns:
        tuple[Path, Path]: import and export directories
    """
    import_dir = Path("./data/import")
    import_dir.mkdir(exist_ok=True, parents=True)
    export_dir = Path("./data/export")
    export_dir.mkdir(exist_ok=True, parents=True)

    return import_dir, export_dir
