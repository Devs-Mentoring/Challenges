from dataclasses import dataclass
from datetime import date


@dataclass
class Event:
    reader_id: int
    book_title: str
    borrow_date: date
    return_date: date
