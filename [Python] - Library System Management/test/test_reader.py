from unittest.mock import Mock, call

from _pytest.fixtures import fixture

from src.abstract_reader import AbstractReader
from src.book import Book
from src.errors import Errors
from src.event_handler import EventHandler
from src.library import Library
from src.library_manager import LibraryManager
from src.reader import Reader


class TestReader:

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
    def reader(self) -> AbstractReader:
        return Reader("John", "Doe", 1)

    @fixture
    def book(self) -> Book:
        return Book("The flight", "Exupery", "Publisher", 1990, 3)

    def test_update(self, reader: AbstractReader, book: Book):
        mock = Mock(reader.update(book), return_value=None)
        mock(1)
        calls = [call(1)]
        mock.assert_has_calls(calls)

    def test_borrow_book(self, library: Library, book: Book, reader: AbstractReader,
                         library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        reader.borrow_book(book)
        assert book in library.books and book.available_copies == 2
        assert len(reader.borrowed_books) == 1

    def test_return_book_removes_book_from_readers_list(self, reader: AbstractReader, book: Book,
                                                        library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        reader.borrow_book(book)
        reader.return_book(book)
        assert len(reader.borrowed_books) == 0

    def test_return_book_adds_available_copies(self, book: Book, reader: AbstractReader, library: Library,
                                               library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        reader.borrow_book(book)
        reader.borrow_book(book)
        reader.return_book(book)
        assert book in library.books and book.available_copies == 2

    def test_reserve_book(self, book: Book, reader: AbstractReader, library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        reader.reserve_book(book)
        assert len(reader.reserved_books) == 1
