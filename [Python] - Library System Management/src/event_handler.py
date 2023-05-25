from datetime import date

from src.abstract_reader import AbstractReader
from src.book import Book
from src.event import Event


class EventHandler:
    def __init__(self):
        self._list_of_events = []

    def _get_return_date(self, reader: AbstractReader, book: Book) -> date:
        for event in self._list_of_events:
            if event.book_title == book.title and event.reader_id == reader.reader_id:
                return event.return_date

    def _check_days_overdue(self, book: Book, reader: AbstractReader, today: date) -> int:
        due_date = self._get_return_date(reader, book)
        if due_date is not None and due_date < today:
            days_overdue = (today - due_date).days
            print(f"Book '{book}' is {days_overdue} days overdue for {str(self)}.")
            return days_overdue
        return 0

    def get_borrow_date(self, reader: AbstractReader, book: Book) -> date:
        for event in self._list_of_events:
            if event.book_title == book.title and event.reader_id == reader.reader_id:
                return event.borrow_date

    def update_history(self, reader: AbstractReader, book: Book, borrow_date: date, return_date: date) -> None:
        event = Event(reader.reader_id, book.title, borrow_date, return_date)
        self._list_of_events.append(event)

    def apply_penalty_for_the_reader(self, book: Book, reader: AbstractReader, today: date) -> None:
        days_overdue = self._check_days_overdue(book, reader, today)
        penalty = days_overdue * 5
        reader._debt = penalty

    def remind(self, book: Book, reader: AbstractReader, today: date) -> int:
        if self._get_return_date(reader, book) > today:
            days_to_return = self._get_return_date(reader, book) - today
            if days_to_return.days <= 3:
                return days_to_return.days

    def display_history(self):
        for event in self._list_of_events:
            print(f"book title: {event.book_title}, reader id: {event.reader_id},"
                  f" borrow date: {event.borrow_date}, return date: {event.return_date} ")
