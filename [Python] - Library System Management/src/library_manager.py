from datetime import date, timedelta

from src.abstract_reader import AbstractReader
from src.book import Book
from src.errors import Errors
from src.event_handler import EventHandler
from src.library import Library


class LibraryManager:
    def __init__(self, error_manager: Errors, event_handler: EventHandler, library: Library):
        self._errors = error_manager
        self._event_handler = event_handler
        self._library = library

    def borrow_book(self, reader: AbstractReader, book: Book, today: date) -> None:
        self._errors.borrow_book(reader, book)
        reader.borrow_book(book)
        self._event_handler.update_history(reader, book, today, today + timedelta(days=14))

    def return_book(self, reader: AbstractReader, book: Book, today: date) -> None:
        self._errors.return_book(reader, book)
        reader.return_book(book)
        self._event_handler.update_history(reader, book, self._event_handler.get_borrow_date(reader, book), today)
        self._event_handler.apply_penalty_for_the_reader(book, reader, today)
        book.notify_subscribers()

    def reserve_book(self, reader: AbstractReader, book: Book) -> None:
        self._errors.reserve_book(reader, book)
        reader.reserve_book(book)
        book.add_subscriber(reader)

    def add_book(self, book: Book) -> None:
        for the_book in self._library.books:
            self._errors.add_book(the_book, book)
        self._library.books.append(book)
        print(f"{str(book)} added.")

    def add_reader(self, reader: AbstractReader) -> None:
        for the_reader in self._library.readers:
            self._errors.add_reader(the_reader, reader)
        self._library.readers.append(reader)
        print(f"{str(reader)} added.")
