from pathlib import Path


EXTENSIONS = [
    ".fit",
    ".fits",
    ".fts"
]


def find_fits(folder):

    folder = Path(folder)

    files = []

    for ext in EXTENSIONS:
        files.extend(folder.glob(f"*{ext}"))

    return sorted(files)