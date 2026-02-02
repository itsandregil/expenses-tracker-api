import io
from csv import DictReader


def normalize_row_helper(row: dict[str, str]) -> dict[str, str]:
    return {k.strip().lower(): v.strip() for k, v in row.items() if k is not None}


def get_reader_from_bytes_helper(contents: bytes):
    return DictReader(io.StringIO(contents.decode("utf-8")))
