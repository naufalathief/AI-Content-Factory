from pathlib import Path


def skip_file(path: str) -> bool:
    file = Path(path)

    if file.exists():
        print(f"Status : SKIP ({file})")
        print()
        return True

    return False


def skip_directory(
    path: str,
    required: str = "metadata.json",
) -> bool:
    folder = Path(path)

    if not folder.exists():
        return False

    marker = folder / required

    if marker.exists():
        print(f"Status : SKIP ({folder})")
        print()
        return True

    return False