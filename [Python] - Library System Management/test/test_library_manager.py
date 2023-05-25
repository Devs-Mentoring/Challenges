from datetime import date

import pytest
from _pytest.fixtures import fixture

from src.abstract_reader import AbstractReader
from src.book import Book
from src.errors import Errors
from src.event_handler import EventHandler
from src.library import Library
from src.library_manager import LibraryManager
from src.reader import Reader


class TestLibraryManager:

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

    def test_borrow_not_existing_book(self, reader: AbstractReader, book: Book, library_manager: LibraryManager) -> None:
        with pytest.raises(ValueError) as e:
            library_manager.borrow_book(reader, book, date(2023, 1, 1))
        assert e.value.args[0] == "Book not added to library."

    def test_borrow_book_already_borrowed(self, library: Library, book: Book, reader: AbstractReader,
                                          library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        library_manager.borrow_book(reader, book, date(2023, 1, 1))
        with pytest.raises(ValueError) as e:
            library_manager.borrow_book(reader, book, date(2023, 1, 1))
        assert e.value.args[0] == "You have already borrowed this book."

    def test_borrow_not_available_book(self, library: Library, book: Book, reader: AbstractReader,
                                       reader2: AbstractReader, reader3: AbstractReader,
                                       library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        library_manager.borrow_book(reader, book, date(2023, 1, 1))
        library_manager.borrow_book(reader2, book, date(2023, 1, 1))
        with pytest.raises(ValueError) as e:
            library_manager.borrow_book(reader3, book, date(2023, 1, 1))
        assert e.value.args[0] == "Book is currently unavailable."

    def test_return_book_which_was_not_borrowed(self, library: Library, book: Book, reader: AbstractReader,
                                                library_manager: LibraryManager) -> None:
        with pytest.raises(ValueError) as e:
            library_manager.return_book(reader, book, date(2023, 1, 1))
        assert e.value.args[0] == "Book is not from this library."

    def test_reserve_borrowed_book(self, library: Library, book: Book, reader: AbstractReader, reader2: AbstractReader,
                                   library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        library_manager.borrow_book(reader, book, date(2023, 1, 1))
        library_manager.borrow_book(reader2, book, date(2023, 1, 1))
        with pytest.raises(ValueError) as e:
            library_manager.reserve_book(reader, book)
        assert e.value.args[0] == "You borrowed this book."

    def test_reserve_already_reserved_book(self, library: Library, book: Book, reader: AbstractReader,
                                           reader2: AbstractReader, reader3: AbstractReader,
                                           library_manager: LibraryManager) -> None:
        library_manager.add_book(book)
        library_manager.borrow_book(reader, book, date(2023, 1, 1))
        library_manager.borrow_book(reader3, book, date(2023, 1, 1))
        library_manager.reserve_book(reader2, book)
        with pytest.raises(ValueError) as e:
            library_manager.reserve_book(reader2, book)
        assert e.value.args[0] == "You have already reserved this book."

    def test_reserve_book_not_added_to_library(self, library: Library, book: Book, reader: AbstractReader,
                                               library_manager: LibraryManager) -> None:
        with pytest.raises(ValueError) as e:
            library_manager.reserve_book(reader, book)
        assert e.value.args[0] == "Book was not added to library."
