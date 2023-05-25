from _pytest.fixtures import fixture

from src.abstract_reader import AbstractReader
from src.book import Book
from src.errors import Errors
from src.library_manager import LibraryManager
from src.reader import Reader
from src.event_handler import EventHandler
from src.library import Library


class TestLibrary:

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

    @fixture
    def reader2(self) -> AbstractReader:
        return Reader("Jane", "Doe", 2)

    @fixture
    def reader3(self) -> AbstractReader:
        return Reader("Mo", "Doe", 2)

    def test_find_book_by_title(self, library: Library, book: Book, library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        assert library.find_book_by_title(book._title) == book

    def test_find_reader_by_id(self, library: Library, reader: AbstractReader, library_manager: LibraryManager) -> None:
        library_manager.add_reader(reader)
        assert library.find_reader_by_id(reader.reader_id) == reader
