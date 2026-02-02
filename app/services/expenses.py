from fastapi import UploadFile
from pydantic import ValidationError
from sqlmodel import Session

from app.models import Expense, ExpenseImport, User
from app.utils import get_reader_from_bytes_helper, normalize_row_helper


def check_is_valid_csv_file(file: UploadFile) -> None:
    if file.filename is None or not file.filename.endswith(".csv"):
        raise ValueError("Invalid CSV file")


def check_file_has_valid_headers(contents: bytes) -> None:
    reader = get_reader_from_bytes_helper(contents)
    headers = reader.fieldnames
    if headers is None:
        raise ValueError("CSV is missing headers")
    required_headers = {"description", "amount", "date", "category"}
    normalized = {header.strip().lower() for header in headers}
    if not required_headers.issubset(normalized):
        missing_headers = required_headers - normalized
        raise ValueError(f"Missing required headers: {missing_headers}")


async def import_expenses_from_csv(*, session: Session, user: User, contents: bytes):
    reader = get_reader_from_bytes_helper(contents)
    for row in reader:
        if not any(row.values()):
            continue
        normalized_row = normalize_row_helper(row)
        try:
            imported = ExpenseImport.model_validate(normalized_row)
            expense = Expense(**imported.model_dump())
            expense.user_id = user.id
            session.add(expense)
        except ValidationError:
            continue
    session.commit()
