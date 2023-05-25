from _pytest.fixtures import fixture

from src.abstract_reader import AbstractReader
from src.book import Book
from src.errors import Errors
from src.event_handler import EventHandler
from src.library import Library
from src.library_facade import LibraryFacade
from src.library_manager import LibraryManager
from src.reader import Reader


class TestLibraryFacade:

    @fixture
    def library_facade(self, library_manager: LibraryManager, event_handler: EventHandler,
                       library: Library) -> LibraryFacade:
        return LibraryFacade(library_manager, event_handler, library)

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

    def test_borrow_not_existing_book(self, reader: AbstractReader, book: Book, library_facade: LibraryFacade) -> None:
        library_facade.borrow_book(reader, book)
        assert len(reader.borrowed_books) == 0

    def test_borrow_book_already_borrowed(self, library: Library, book: Book, reader: AbstractReader,
                                          library_facade: LibraryFacade) -> None:
        library_facade.add_book(book)
        library_facade.borrow_book(reader, book)
        library_facade.borrow_book(reader, book)
        assert len(reader.borrowed_books) == 1

    def test_borrow_not_available_book(self, library: Library, book: Book, reader: AbstractReader,
                                       reader2: AbstractReader, reader3: AbstractReader,
                                       library_facade: LibraryFacade) -> None:
        library_facade.add_book(book)
        library_facade.borrow_book(reader, book)
        library_facade.borrow_book(reader2, book)
        library_facade.borrow_book(reader3, book)
        assert len(reader3.borrowed_books) == 0

    def test_return_book_which_was_not_borrowed(self, library: Library, book: Book, reader: AbstractReader,
                                                library_facade: LibraryFacade) -> None:
        library_facade.return_book(reader, book)
        assert book.available_copies == 2

    def test_reserve_borrowed_book(self, library: Library, book: Book, reader: AbstractReader,
                                   library_facade: LibraryFacade) -> None:
        library_facade.add_book(book)
        library_facade.borrow_book(reader, book)
        library_facade.reserve_book(reader, book)
        assert len(reader.reserved_books) == 0

    def test_reserve_already_reserved_book(self, library: Library, book: Book, reader: AbstractReader,
                                           reader2: AbstractReader, reader3: AbstractReader,
                                           library_facade: LibraryFacade) -> None:
        library_facade.add_book(book)
        library_facade.borrow_book(reader, book)
        library_facade.borrow_book(reader3, book)
        library_facade.reserve_book(reader2, book)
        library_facade.reserve_book(reader2, book)
        assert len(reader.reserved_books) == 0

    def test_reserve_book_not_added_to_library(self, library: Library, book: Book, reader: AbstractReader,
                                               library_facade: LibraryFacade) -> None:
        library_facade.reserve_book(reader, book)
        assert len(reader.reserved_books) == 0

    def test_add_book(self, library: Library, book: Book, library_facade: LibraryFacade) -> None:
        library_facade.add_book(book)
        assert book in library.books

    def test_add_existing_book(self, library: Library, book: Book, library_facade: LibraryFacade) -> None:
        library_facade.add_book(book)
        library_facade.add_book(book)
        assert len(library.books) == 1

    def test_add_reader(self, library: Library, reader: AbstractReader, library_facade: LibraryFacade) -> None:
        library_facade.add_reader(reader)
        assert len(library.readers) == 1

    def test_add_existing_reader(self, library: Library, reader: AbstractReader, library_facade: LibraryFacade) -> None:
        library_facade.add_reader(reader)
        library_facade.add_reader(reader)
        assert len(library.readers) == 1
