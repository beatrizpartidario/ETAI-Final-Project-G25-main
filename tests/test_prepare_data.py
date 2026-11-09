from pathlib import Path
from zipfile import ZipFile

import pytest

from src.prepare_data import EXPECTED, prepare_data


def test_extract_only_expected_files(tmp_path: Path) -> None:
    archive = tmp_path / "data.zip"
    with ZipFile(archive, "w") as zf:
        for name in EXPECTED:
            zf.writestr(f"Project_data/{name}", "ID\n1\n")
        zf.writestr("../should_not_extract.txt", "unsafe")
    destination = tmp_path / "raw"
    result = prepare_data(archive, destination)
    assert {p.name for p in result} == set(EXPECTED)
    assert all(p.read_text() == "ID\n1\n" for p in result)
    assert not (tmp_path / "should_not_extract.txt").exists()
    with pytest.raises(FileExistsError):
        prepare_data(archive, destination)


def test_missing_expected_file_fails(tmp_path: Path) -> None:
    archive = tmp_path / "incomplete.zip"
    with ZipFile(archive, "w") as zf:
        zf.writestr("Project_data/train.csv", "ID\n1\n")
    with pytest.raises(ValueError, match="missing required"):
        prepare_data(archive, tmp_path / "raw")
