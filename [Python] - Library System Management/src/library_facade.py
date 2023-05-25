from datetime import date

from src.abstract_reader import AbstractReader
from src.book import Book
from src.event_handler import EventHandler
from src.library import Library
from src.library_manager import LibraryManager


class LibraryFacade:
    def __init__(self, library_manager: LibraryManager, event_handler: EventHandler, library: Library):
        self._library_manager = library_manager
        self._event_handler = event_handler
        self._library = library

    def borrow_book(self, reader: AbstractReader, book: Book) -> None:
        try:
            self._library_manager.borrow_book(reader, book, date.today())
        except ValueError as e:
            print(e)

    def return_book(self, reader: AbstractReader, book: Book) -> None:
        try:
            self._library_manager.return_book(reader, book, date.today())
        except ValueError as e:
            print(e)

    def reserve_book(self, reader: AbstractReader, book: Book) -> None:
        try:
            self._library_manager.reserve_book(reader, book)
        except ValueError as e:
            print(e)

    def add_book(self, book: Book) -> None:
        try:
            self._library_manager.add_book(book)
        except ValueError as e:
            print(e)

    def add_reader(self, reader: AbstractReader) -> None:
        try:
            self._library_manager.add_reader(reader)
        except ValueError as e:
            print(e)

    def display_history(self) -> None:
        self._event_handler.display_history()

    def display_all_books(self) -> None:
        self._library.display_all_books()

    def display_all_readers(self) -> None:
        self._library.display_all_readers()

    def find_reader_by_id(self, reader_id) -> None:
        self._library.find_reader_by_id(reader_id)

    def find_book_by_title(self, book_title) -> None:
        self._library.find_book_by_title(book_title)

    def remind(self, reader: AbstractReader, book: Book) -> None:
        self._event_handler.remind(book, reader, date.today())

