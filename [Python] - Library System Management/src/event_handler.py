from datetime import date

from src.book import Book
from src.event import Event
from src.library import Library
from src.reader import Reader


class EventHandler:
    def __init__(self):
        self._list_of_events = []

    def _get_return_date(self, reader: Reader, book: Book) -> date:
        for event in self._list_of_events:
            if event.book_title == book.title and event.reader_name == reader.name:
                return event.return_date

    def _check_days_overdue(self, book: Book, reader: Reader, today: date) -> int:
        due_date = self._get_return_date(reader, book)
        if due_date is not None and due_date < today:
            days_overdue = (today - due_date).days
            print(f"Book '{book}' is {days_overdue} days overdue for {str(self)}.")
            return days_overdue
        return 0

    def get_borrow_date(self, reader: Reader, book: Book) -> date:
        for event in self._list_of_events:
            if event.book_title == book.title and event.reader_name == reader.name:
                return event.borrow_date

    def update_history(self, reader: Reader, book: Book, borrow_date: date, return_date: date) -> None:
        event = Event(reader.name, book.title, borrow_date, return_date)
        self._list_of_events.append(event)

    def apply_penalty_for_the_reader(self, book: Book, reader: Reader, today: date) -> None:
        days_overdue = self._check_days_overdue(book, reader, today)
        penalty = days_overdue * 5
        reader.debt = penalty

    def remind(self, reader: Reader, today: date) -> None:
        for book in reader.books:
            if self._get_return_date(reader, book) > today:
                days_to_return = self._get_return_date(reader, book) - today
                print(f"You have {days_to_return} to return {book.title}.")

    def display_history(self):
        print("List of all events:")
        for event in self._list_of_events:
            print(f"book title: {event.book_title}, reader name: {event.reader_name},"
                  f" borrow date: {event.borrow_date}, return date: {event.return_date} ")

    def notify_subscribers(self, library: Library, reader: Reader) -> None:
        for book in library.books:
            if book.available is True and book in reader.reserved_books:
                reader.update(book)
