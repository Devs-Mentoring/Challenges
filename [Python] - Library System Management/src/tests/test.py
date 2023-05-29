import pytest
from datetime import datetime, timedelta
from main import Library, Book, Reader

@pytest.fixture
def library():
    lib = Library()
    lib.add_book("Test Book", "John Doe", "Test Publisher", 2023, 1)
    lib.add_reader("John", "Doe")
    lib.add_reader('Joe', 'Foe')
    return lib

def test_add_book(library):
    assert len(library.book_manager.books) == 1
    assert isinstance(list(library.book_manager.books.values())[0], Book)
    assert list(library.book_manager.books.values())[0].title == "Test Book"

def test_add_reader(library):
    assert len(library.reader_manager.readers) == 2
    assert isinstance(list(library.reader_manager.readers.values())[0], Reader)
    assert list(library.reader_manager.readers.values())[0].name == "John"

def test_borrow_book(library):
    book_id = list(library.book_manager.books.keys())[0]
    reader_id = list(library.reader_manager.readers.keys())[0]
    library.borrow_book(book_id, reader_id)

    reader = library.reader_manager.get_reader(reader_id)
    assert len(reader.borrowed_books) == 1
    assert isinstance(list(reader.borrowed_books.keys())[0], Book)

def test_return_book(library):
    book_id = list(library.book_manager.books.keys())[0]
    reader_id = list(library.reader_manager.readers.keys())[0]
    library.borrow_book(book_id, reader_id)
    library.return_book(book_id, reader_id)

    reader = library.reader_manager.get_reader(reader_id)
    assert len(reader.borrowed_books) == 0

def test_book_reservation(library):
    book_id = list(library.book_manager.books.keys())[0]
    reader_id = list(library.reader_manager.readers.keys())[0]
    library.borrow_book(book_id, reader_id)
    reader_id = list(library.reader_manager.readers.keys())[1]
    library.borrow_book(book_id, reader_id)


    book = library.book_manager.get_book(book_id)
    assert len(book.reservations) == 1


