from datetime import date

from _pytest.fixtures import fixture

from src.abstract_reader import AbstractReader
from src.book import Book
from src.errors import Errors
from src.event_handler import EventHandler
from src.library import Library
from src.library_manager import LibraryManager
from src.reader import Reader


class TestEventHandler:

    @fixture
    def event_handler(self) -> EventHandler:
        return EventHandler()

    @fixture
    def errors(self, library: Library) -> Errors:
        return Errors(library)

    @fixture
    def library_manager(self, errors, event_handler, library) -> LibraryManager:
        return LibraryManager(errors, event_handler, library)

    @fixture
    def library(self, event_handler: EventHandler) -> Library:
        return Library([], [])

    @fixture
    def book(self) -> Book:
        return Book("The flight", "Exupery", "Publisher", 1990, 2)

    @fixture
    def reader(self) -> AbstractReader:
        return Reader("John", "Doe", 1)

    def test_update_history(self, book: Book, reader: AbstractReader,
                            event_handler: EventHandler, library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        library_manager.borrow_book(reader, book, date(2023, 1, 1))
        library_manager.return_book(reader, book, date(2023, 1, 3))
        assert len(event_handler._list_of_events) == 2

    def test_apply_penalty_for_the_reader(self, book: Book, reader: AbstractReader,
                                          event_handler: EventHandler, library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        library_manager.borrow_book(reader, book, date(2023, 1, 1))
        library_manager.return_book(reader, book, date(2023, 1, 16))
        assert reader.debt == 5

    def test_remind(self, book: Book, reader: AbstractReader, event_handler: EventHandler,
                    library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        library_manager.borrow_book(reader, book, date(2023, 1, 1))
        assert event_handler.remind(book, reader, date(2023, 1, 12)) == 3

    def test_get_borrow_date(self, book: Book, reader: AbstractReader, event_handler: EventHandler,
                             library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        library_manager.borrow_book(reader, book, date(2023, 1, 1))
        assert event_handler.get_borrow_date(reader, book) == date(2023, 1, 1)
