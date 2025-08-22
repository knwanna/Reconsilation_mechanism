import pytest
import pandas as pd
from adapters.repositories.csv_repository import CsvRepository
from core.domain.models import Record

def test_csv_repository_get_all_records(tmp_path):
    csv_content = """id,title,author,year,canonical_id
1,The Hobbit,J.R.R. Tolkien,1937,tolkien-1
2,1984,George Orwell,1949,orwell-1"""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    repo = CsvRepository(str(csv_file))
    records = repo.get_all_records()

    assert len(records) == 2
    assert records[0] == Record(id=1, title="The Hobbit", author="J.R.R. Tolkien", year=1937, canonical_id="tolkien-1")
    assert records[1] == Record(id=2, title="1984", author="George Orwell", year=1949, canonical_id="orwell-1")

def test_csv_repository_file_not_found(tmp_path):
    repo = CsvRepository(str(tmp_path / "nonexistent.csv"))
    with pytest.raises(FileNotFoundError):
        repo.get_all_records()
