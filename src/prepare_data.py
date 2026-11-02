"""Safely extract only the four expected CSV files from the supplied assignment ZIP."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = (
    "clientes.csv",
    "sample_submission.csv",
    "test.csv",
    "train.csv",
)


def prepare_data(archive: Path, destination: Path, *, overwrite: bool = False) -> list[Path]:
    archive = archive.expanduser().resolve()
    destination = destination.expanduser().resolve()
    if not archive.is_file():
        raise FileNotFoundError(f"Archive not found: {archive}")

    with ZipFile(archive) as zf:
        # Explicit internal filenames: no untrusted ZIP paths are used as output paths.
        members = {}
        for member in zf.namelist():
            if member in {f"Project_data/{name}" for name in EXPECTED}:
                members[Path(member).name] = member
        missing = sorted(set(EXPECTED) - set(members))
        if missing:
            raise ValueError(f"Archive is missing required files: {missing}")
        existing = [destination / name for name in EXPECTED if (destination / name).exists()]
        if existing and not overwrite:
            raise FileExistsError(
                "Data already exists. Pass --overwrite only if you intend to replace: "
                + ", ".join(str(p) for p in existing)
            )
        destination.mkdir(parents=True, exist_ok=True)
        paths = []
        for name in EXPECTED:
            output = destination / name
            with zf.open(members[name]) as source, output.open("wb") as sink:
                import shutil
                shutil.copyfileobj(source, sink)
            paths.append(output)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True, help="Original project ZIP path")
    parser.add_argument("--destination", type=Path, default=ROOT / "data" / "raw")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    for path in prepare_data(args.archive, args.destination, overwrite=args.overwrite):
        print(f"Extracted: {path}")
    print("Raw datasets are ignored by Git. Keep the source ZIP in a safe place.")


if __name__ == "__main__":
    main()
